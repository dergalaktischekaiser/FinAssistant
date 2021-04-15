package servlets;

import javax.servlet.http.HttpServletRequest;

import db_service.DBService;
import db_service.DBServiceException;
import model.DBResponse;
import token.TokenMatchingException;
import token.TokenUtils;
import token.TokensResponse;

import static java.lang.String.format;

public class ApiGenerateToken extends ApiServlet {
    public ApiGenerateToken(DBService service, TokenUtils tokenUtils) {
        super(service, tokenUtils);
    }

    @Override
    protected DBResponse doPostInternal(HttpServletRequest req) throws DBServiceException, TokenMatchingException {
        String refreshToken = req.getHeader(REFRESH_TOKEN_HEADER);
        if (refreshToken == null) {
            throw new TokenMatchingException(format("Refresh token was not found in %s header", REFRESH_TOKEN_HEADER));
        }
        if (refreshToken.equals("")) {
            throw new TokenMatchingException(format("Refresh token is empty in %s header", REFRESH_TOKEN_HEADER));
        }
        long userId = service.getUserIdByRefreshToken(refreshToken);
        TokensResponse tokens = tokenUtils.generateTokens(userId);
        service.updateRefreshToken(userId, tokens.getRefreshToken());

        return tokens;
    }

    @Override
    protected String requestDescription() {
        return "auth/refresh";
    }
}
