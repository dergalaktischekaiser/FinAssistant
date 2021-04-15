package model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class SuccessResponse extends DBResponse {
    private final DBResponse data;

    public SuccessResponse(DBResponse data) {
        super("");
        this.data = data;
    }

    @JsonProperty("data")
    public DBResponse getData() {
        return data;
    }
}