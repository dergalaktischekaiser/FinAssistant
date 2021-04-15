package servlets;

import java.io.IOException;
import java.util.Arrays;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.auth0.jwt.interfaces.DecodedJWT;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.base.Charsets;
import com.google.common.net.MediaType;
import com.mashape.unirest.http.exceptions.UnirestException;
import db_service.DBService;
import db_service.DBServiceException;
import model.DBResponse;
import model.SuccessResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import token.TokenMatchingException;
import token.TokenUtils;
//import org.slf4j.Logger;
//import org.slf4j.LoggerFactory;

import static model.DBResponse.error;
import static model.DBResponse.success;

public class ApiServlet extends HttpServlet {
    private static final Logger LOG = LoggerFactory.getLogger(ApiServlet.class);

    //private static final Logger LOG = LoggerFactory.getLogger(ApiServlet.class);
    public static final String ACCESS_TOKEN_HEADER = "X-Auth-Access";
    public static final String REFRESH_TOKEN_HEADER = "X-Auth-Refresh";

    protected final ObjectMapper jsonMapper = new ObjectMapper();
    protected final DBService service;
    protected final TokenUtils tokenUtils;

    public ApiServlet(DBService service, TokenUtils tokenUtils) {
        this.service = service;
        this.tokenUtils = tokenUtils;
    }

    private enum QueryType {
        POST("POST"),
        GET("GET"),
        DELETE("DELETE");

        private final String name;

        QueryType(String name) {
            this.name = name;
        }

        public String getName() {
            return name;
        }
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        doCore(req, resp, QueryType.POST);
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        doCore(req, resp, QueryType.GET);
    }

    @Override
    protected void doDelete(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        doCore(req, resp, QueryType.DELETE);
    }

    private void doCore(HttpServletRequest req, HttpServletResponse resp, QueryType queryType)
        throws IOException {
        prepareResponse(resp);
        System.out.println(String.format("Start processing %s request '%s'", queryType.getName(), requestDescription()));
        try {
            DBResponse dbResponse;
            switch (queryType) {
                case GET:
                    dbResponse = doGetInternal(req);
                    break;
                case POST:
                    dbResponse = doPostInternal(req);
                    break;
                case DELETE:
                    dbResponse = doDeleteInternal(req);
                    break;
                default:
                    dbResponse = new DBResponse("Unexpected query type");
            }
            writeSuccessResponse(dbResponse, resp);
        } catch (Throwable exception) {
            System.out.println("****" + Arrays.toString(exception.getStackTrace()));
            writeErrorResponse(exception, resp, queryType.getName());
        }
    }

    protected DBResponse doPostInternal(HttpServletRequest req)
        throws IOException, DBServiceException, UnirestException, TokenMatchingException {
        return success();
    }

    protected DBResponse doGetInternal(HttpServletRequest req) throws DBServiceException, TokenMatchingException {
        return success();
    }

    protected DBResponse doDeleteInternal(HttpServletRequest req)
        throws IOException, TokenMatchingException, DBServiceException {
        return success();
    }

    protected String requestDescription() {
        return "";
    }

    protected String getStringParameter(HttpServletRequest req, String name) {
        String param = req.getParameter(name);
        return param == null ? "" : param;
    }

    private void prepareResponse(HttpServletResponse response) {
        response.setCharacterEncoding(Charsets.UTF_8.name());
        response.setContentType(MediaType.JSON_UTF_8.toString());
    }

    private void writeSuccessResponse(DBResponse dbResponse, HttpServletResponse response) throws IOException {
        String dbResponseStr = responseToString(new SuccessResponse(dbResponse));
        if (!dbResponseStr.isEmpty()) {
            response.getWriter().print(dbResponseStr);
        }
        response.setStatus(200);
    }

    private void writeErrorResponse(Throwable error, HttpServletResponse response, String requestType)
        throws IOException {
        System.out.printf("Error while %s request '%s': %s%n", requestType, requestDescription(), error.getCause());
        LOG.error("Error while {} request '{}'", requestType, requestDescription(), error.getCause());

        response.getWriter().print(responseToString(error(error.getMessage())));
        response.setStatus(400);
    }

    private String responseToString(DBResponse DBResponse) throws IOException {
        return jsonMapper.writerWithDefaultPrettyPrinter().writeValueAsString(DBResponse);
    }

    protected int getUserId(DecodedJWT decodedJWT) {
        return decodedJWT.getClaim("user_id").asInt();
    }

    protected DecodedJWT verifyToken(HttpServletRequest req) throws TokenMatchingException {
        return tokenUtils.verifyAccessToken(req.getHeader(ACCESS_TOKEN_HEADER));
    }
}
