package servlets;

import javax.servlet.http.HttpServletRequest;

import db_service.DBService;
import db_service.DBServiceException;
import model.DBResponse;
import token.TokenMatchingException;
import token.TokenUtils;

public class ApiGetUser extends ApiServlet{
    public ApiGetUser(DBService service, TokenUtils tokenUtils) {
        super(service, tokenUtils);
    }

    @Override
    protected DBResponse doGetInternal(HttpServletRequest req) throws DBServiceException, TokenMatchingException {
        long userId = getUserId(verifyToken(req));
        return service.getUser(userId);
    }

    @Override
    protected String requestDescription() {
        return "me";
    }
}
