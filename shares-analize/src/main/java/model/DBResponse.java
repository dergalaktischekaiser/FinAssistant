package model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class DBResponse {
    private final String errorMessage;

    public DBResponse(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public static DBResponse success() {
        return new DBResponse("");
    }

    public static DBResponse error(String errorMessage) {
        return new DBResponse(errorMessage);
    }

    @JsonProperty("error_message")
    public String getErrorMessage() {
        return errorMessage;
    }
}
