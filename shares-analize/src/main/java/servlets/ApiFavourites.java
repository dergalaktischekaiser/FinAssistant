package servlets;

import java.io.IOException;

import javax.servlet.http.HttpServletRequest;

import db_service.DBServiceException;
import db_service.DBServiceImpl;
import model.ChangeFavouritesRequest;
import model.DBResponse;
import model.FavouritesResponse;
import token.TokenMatchingException;
import token.TokenUtils;

public class ApiFavourites extends ApiServlet {

    public ApiFavourites(DBServiceImpl dbService, TokenUtils tokenUtils) {
        super(dbService, tokenUtils);
    }

    @Override
    protected DBResponse doPostInternal(HttpServletRequest req)
        throws IOException, TokenMatchingException, DBServiceException {
        int userId = getUserId(verifyToken(req));
        ChangeFavouritesRequest request = jsonMapper.readValue(req.getReader(), ChangeFavouritesRequest.class);
        service.addFavourite(userId, request);
        return DBResponse.success();
    }

    @Override
    protected DBResponse doDeleteInternal(HttpServletRequest req)
        throws IOException, TokenMatchingException, DBServiceException {
        int userId = getUserId(verifyToken(req));
        ChangeFavouritesRequest request = jsonMapper.readValue(req.getReader(), ChangeFavouritesRequest.class);
        service.removeFavourite(userId, request);
        return DBResponse.success();
    }

    @Override
    protected String requestDescription() {
        return "favourites";
    }
}
