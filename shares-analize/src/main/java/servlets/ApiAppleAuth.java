package servlets;

import java.io.IOException;
import java.util.Optional;

import javax.servlet.http.HttpServletRequest;

import authorization.apple.AppleAuthorization;
import com.mashape.unirest.http.exceptions.UnirestException;
import db_service.DBService;
import db_service.DBServiceException;
import model.AppleAuthRequest;
import model.CreateUserRequest;
import model.DBResponse;
import model.UserResponse;
import token.TokenUtils;
import token.TokensResponse;

public class ApiAppleAuth extends ApiServlet{
    public ApiAppleAuth(DBService service, TokenUtils tokenUtils) {
        super(service, tokenUtils);
    }

    @Override
    protected DBResponse doPostInternal(HttpServletRequest req) throws IOException, DBServiceException, UnirestException {
        AppleAuthRequest request = jsonMapper.readValue(req.getReader(), AppleAuthRequest.class);
        String appleId = request.getToken();//AppleAuthorization.auth(request.getToken());
        Optional<UserResponse> userResponseOpt = service.getUserByRegistrationServiceId("apple_id", appleId);
        if (userResponseOpt.isPresent()) {
            long userId = userResponseOpt.get().getId();
            TokensResponse tokens = tokenUtils.generateTokens(userId);
            service.updateRefreshToken(userId, tokens.getRefreshToken());
            return tokens;
        } else {
            String refreshToken = tokenUtils.generateRefreshToken();
            CreateUserRequest createUserRequest = new CreateUserRequest(
                request.getUserName(), refreshToken, appleId);
            long userId = service.addUser(createUserRequest);

            return new TokensResponse(tokenUtils.generateAccessToken(userId), refreshToken);
        }

    }

    @Override
    protected String requestDescription() {
        return "auth/apple";
    }
}
