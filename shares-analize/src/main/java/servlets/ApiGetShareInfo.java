package servlets;

import java.io.IOException;
import java.util.concurrent.ExecutionException;

import javax.servlet.http.HttpServletRequest;

import db_service.DBService;
import db_service.DBServiceException;
import model.DBResponse;
import model.StockResponse;
import token.TokenUtils;


public class ApiGetShareInfo extends ApiServlet {
    public ApiGetShareInfo(DBService service, TokenUtils tokenUtils) {
        super(service, tokenUtils);
    }

    @Override
    protected DBResponse doGetInternal(HttpServletRequest req) throws DBServiceException {
        String tickerId = getStringParameter(req, "ticker");
        String consistence = getStringParameter(req, "consistence");
        StockResponse stockResponse = service.getStockOverview(tickerId);
        stockResponse.setConsistence(consistence);
        return stockResponse;
    }

    @Override
    protected String requestDescription() {
        return "overview";
    }

}
