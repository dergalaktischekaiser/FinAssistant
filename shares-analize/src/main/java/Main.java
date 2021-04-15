import java.sql.SQLException;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import javax.servlet.http.HttpServlet;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.base.Throwables;
import com.google.common.collect.ImmutableMap;
import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;
import db_service.DBServiceImpl;
import org.eclipse.jetty.server.Handler;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.ServerConnector;
import org.eclipse.jetty.server.handler.DefaultHandler;
import org.eclipse.jetty.server.handler.HandlerCollection;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.eclipse.jetty.util.thread.QueuedThreadPool;
import servlets.ApiAppleAuth;
import servlets.ApiFavourites;
import servlets.ApiGenerateToken;
import servlets.ApiGetShareInfo;
import servlets.ApiGetUser;
import token.TokenUtils;

import static java.lang.System.exit;

public class Main {
    private static final ObjectMapper mapper = new ObjectMapper();

    public static void main(String[] args) throws ClassNotFoundException {
        Config config = ConfigFactory.load("default_config.conf");
        Class.forName("org.postgresql.Driver");
        String DB_URL = "jdbc:postgresql://ec2-54-216-155-253.eu-west-1.compute.amazonaws.com:5432/d5fre91hfg8vvf";
        String DB_PASSWORD = "bc4f2354ca29efd58e6dada90d8ca8c44203e69c0a41ef702b22e739dc7d8cda";
        String DB_USER = "yhxvtdvlnvmtxs";
        try {
            DBServiceImpl dbService = new DBServiceImpl(DB_URL, DB_USER, DB_PASSWORD);
            TokenUtils tokenUtils = new TokenUtils("PrivateKey");
            runHttpServers(config, dbService, tokenUtils);
        } catch (SQLException exception) {
            System.err.println("Error in main: " + exception);
            exit(1);
        }
    }

    private static void runHttpServers(Config config, DBServiceImpl dbService, TokenUtils tokenUtils) {
        try {
            for (Server server : getServers(config.getConfig("http_server"), dbService, tokenUtils)) {
                server.start();
            }
        } catch (Exception e) {
            Throwables.throwIfUnchecked(e);
            throw new RuntimeException(e);
        }
    }

    private static Server buildServer(Config config, Map<String, HttpServlet > servlets) {
        int workerThreads = config.getInt("worker_threads");
        Server server = new Server(new QueuedThreadPool(workerThreads, workerThreads));

        int selectorThreads = config.getInt("selector_threads");
        String portEnv = System.getenv("PORT");
        int port = portEnv == null ? config.getInt("port") : Integer.parseInt(portEnv);
        ServerConnector connector = new ServerConnector(server, 0, selectorThreads);
        connector.setReuseAddress(true);
        connector.setHost("::");
        connector.setPort(port);
        connector.setIdleTimeout(config.getDuration("connection_timeout", TimeUnit.MILLISECONDS));
        connector.setAcceptQueueSize(config.getInt("accept_backlog_size"));
        server.addConnector(connector);

        ServletContextHandler context = new ServletContextHandler();
        context.setContextPath("/");
        String rootPath = config.getString("root_path");
        servlets.forEach((name, servlet) -> {
            System.out.println(String.format("Listen(%d): %s", port, rootPath + name));
            context.addServlet(new ServletHolder(servlet), rootPath + name);
        });
        HandlerCollection handlers = new HandlerCollection();
        handlers.setHandlers(new Handler[]{context, new DefaultHandler()});
        server.setHandler(handlers);
        return server;
    }

    private static List<Server> getServers(Config config, DBServiceImpl dbService, TokenUtils tokenUtils) {
        Map<String, Map<String, HttpServlet>> servlets = ImmutableMap.of(
            "public_api", ImmutableMap.<String, HttpServlet>builder()
                .put("overview", new ApiGetShareInfo(dbService, tokenUtils))
                .put("favourites", new ApiFavourites(dbService, tokenUtils))
                .put("auth/apple", new ApiAppleAuth(dbService, tokenUtils))
                .put("auth/refresh", new ApiGenerateToken(dbService, tokenUtils))
                .put("me", new ApiGetUser(dbService, tokenUtils))
                .build());

        return config.root().keySet().stream()
            .map(entry -> buildServer(config.getConfig(entry), servlets.get(entry)))
            .collect(Collectors.toList());
    }
}
