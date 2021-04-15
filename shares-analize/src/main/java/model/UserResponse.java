package model;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import java.util.Objects;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class UserResponse extends DBResponse {
    private final long id;
    private final String name;
    private List<FavouriteStockResponse> favouriteStocks;

    public UserResponse(long id, String name) {
        super("");
        this.id = id;
        this.name = name;
    }

    public static UserResponse create(ResultSet resultSet) throws SQLException {
        return new UserResponse(
            resultSet.getInt("id"),
            resultSet.getString("name"));
    }

    @JsonProperty("id")
    public long getId() {
        return id;
    }

    @JsonProperty("name")
    public String getName() {
        return name;
    }

    @JsonProperty("favourite_stocks")
    public List<FavouriteStockResponse> getFavouriteStocks() {
        return favouriteStocks;
    }

    public void setFavouriteStocks(List<FavouriteStockResponse> favouriteStocks) {
        this.favouriteStocks = favouriteStocks;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        UserResponse that = (UserResponse) o;
        return id == that.id &&
            Objects.equals(name, that.name) &&
            Objects.equals(favouriteStocks, that.favouriteStocks);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, name, favouriteStocks);
    }

}
