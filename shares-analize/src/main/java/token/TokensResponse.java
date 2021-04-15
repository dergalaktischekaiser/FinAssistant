package token;

import com.fasterxml.jackson.annotation.JsonProperty;
import model.DBResponse;

public class TokensResponse extends DBResponse {
    private final String accessToken;
    private final String refreshToken;

    public TokensResponse(String accessToken, String refreshToken) {
        super("");
        this.accessToken = accessToken;
        this.refreshToken = refreshToken;
    }

    @JsonProperty("access_token")
    public String getAccessToken() {
        return accessToken;
    }

    @JsonProperty("refresh_token")
    public String getRefreshToken() {
        return refreshToken;
    }
}
