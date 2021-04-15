package model;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.Date;

import com.fasterxml.jackson.annotation.JsonProperty;

public class FavouriteStockResponse extends DBResponse {
    private final StockResponse stockOverview;
    private final double initialPrice;
    private final Timestamp addedAt;

    public FavouriteStockResponse(StockResponse stockOverview, double initialPrice, Timestamp addedAt) {
        super("");
        this.stockOverview = stockOverview;
        this.initialPrice = initialPrice;
        this.addedAt = addedAt;
    }

    static public FavouriteStockResponse create(ResultSet resultSet) throws SQLException {
        return new FavouriteStockResponse(
            StockResponse.create(resultSet),
            resultSet.getDouble("initial_price"),
            resultSet.getTimestamp("added_at"));
    }

    @JsonProperty("stock_overview")
    public StockResponse getStockOverview() {
        return stockOverview;
    }

    @JsonProperty("initial_price")
    public double getInitialPrice() {
        return initialPrice;
    }

    @JsonProperty("delta_value")
    public double getDeltaValue() {
        return stockOverview.getPrice() - initialPrice;
    }

    @JsonProperty("delta_percent")
    public double getDeltaPercent() {
        return getDeltaValue() / (initialPrice / 100);
    }

    @JsonProperty("added_at")
    public Date getAddedAt() {
        return addedAt;
    }
}
