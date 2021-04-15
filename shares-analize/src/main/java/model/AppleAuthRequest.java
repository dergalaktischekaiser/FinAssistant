package model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class AppleAuthRequest {
    private final String token;
    private final String userName;
    private final String userMail;

    public AppleAuthRequest(
        @JsonProperty("token") String token,
        @JsonProperty("user_name") String userName,
        @JsonProperty("user_email") String userMail) {
        this.token = token;
        this.userName = userName;
        this.userMail = userMail;
    }

    public String getToken() {
        return token;
    }

    public String getUserName() {
        return userName;
    }

    public String getUserMail() {
        return userMail;
    }
}
