package model;

import org.apache.commons.lang3.builder.ToStringBuilder;

public class CreateUserRequest {
    private final String name;
    private final String refreshToken;
    private final String appleId;

    public CreateUserRequest(String name, String refreshToken, String appleId) {
        this.name = name;
        this.appleId = appleId;
        this.refreshToken = refreshToken;
    }

    public String getName() {
        return name;
    }

    public String getAppleId() {
        return appleId;
    }

    public String getRefreshToken() {
        return refreshToken;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this)
            .append("name", name)
            .append("appleId", appleId)
            .toString();
    }
}
