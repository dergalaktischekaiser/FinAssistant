package db_service;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import model.ChangeFavouritesRequest;
import model.ChartEntry;
import model.CreateUserRequest;
import model.FavouriteStockResponse;
import model.StockResponse;
import model.UserResponse;

import static java.lang.String.format;

public class DBServiceImpl implements DBService {
    private final String url;
    private final String user;
    private final String password;
    private final Connection connection;

    public DBServiceImpl(String url, String user, String password) throws SQLException {
        this.url = url;
        this.user = user;
        this.password = password;
        this.connection = DriverManager.getConnection(url, user, password);
    }

    @Override
    public void addFavourite(int userId, ChangeFavouritesRequest request) throws DBServiceException {
/*
        Set<String> favourites = deviceToFavourites.getOrDefault(request.getDeviceId(), new HashSet<>());
        favourites.add(request.getTicker());
        deviceToFavourites.put(request.getDeviceId(), favourites);
*/

        String company = request.getCompany();
        try (Statement statement = connection.createStatement()) {
            statement.executeUpdate(format("INSERT INTO User_To_Favourite_Stocks(user_id, stock_name, initial_price) "
                + "SELECT %d, '%s', price FROM Stock_Data WHERE company='%s'", userId, company, company));
        } catch (SQLException throwable) {
            throw new DBServiceException(
                format("Error while adding favourite company '%s' for user %d", company, userId), throwable);
        }
    }

    @Override
    public void removeFavourite(int userId, ChangeFavouritesRequest request) throws DBServiceException {
/*
        if (!deviceToFavourites.containsKey(request.getDeviceId())) {
            return;
        }
        Set<String> favourites = deviceToFavourites.get(request.getDeviceId());
        favourites.remove(request.getTicker());
        deviceToFavourites.put(request.getDeviceId(), favourites);
*/

        String company = request.getCompany();
        try (Statement statement = connection.createStatement()) {
            statement.executeUpdate(
                format("DELETE FROM User_To_Favourite_Stocks WHERE user_id=%d and stock_name='%s'", userId, company));
        } catch (SQLException throwable) {
            throw new DBServiceException(
                format("Error while removing favourite company '%s' for user %d", company, userId), throwable);
        }

    }

    @Override
    public void updateRefreshToken(long userId, String refreshToken) throws DBServiceException {
        try (Statement statement = connection.createStatement()) {
            statement.executeUpdate(format("UPDATE Users SET refresh_token = '%s' WHERE id=%d", refreshToken, userId));
        } catch (SQLException throwable) {
            throw new DBServiceException(format("Error while updating refresh token for user %d", userId), throwable);
        }
    }

    private List<FavouriteStockResponse> getFavouriteStocksForUserId(Statement statement, long userId)
        throws SQLException, DBServiceException {
        List<FavouriteStockResponse> stocks = new ArrayList<>();
        ResultSet favouriteStocksRs = statement.executeQuery(
            format(
                "SELECT * FROM User_To_Favourite_Stocks JOIN Stock_Data ON User_To_Favourite_Stocks.stock_name = Stock_Data.company "
                    + "WHERE User_To_Favourite_Stocks.user_id = %d", userId));

        while (favouriteStocksRs.next()) {
            try {
                favouriteStocksRs.getString("company");
            } catch (SQLException exception) {
                throw new DBServiceException(
                    format("Company %s does not exist but has reference in User_To_Favourite_Stocks table",
                        favouriteStocksRs.getString("stock_name")));
            }
            stocks.add(FavouriteStockResponse.create(favouriteStocksRs));
        }
        for (FavouriteStockResponse favouriteStockResponse : stocks) {
            StockResponse stockResponse = favouriteStockResponse.getStockOverview();
            stockResponse.set5MinChart(getChart(statement, "Stock_To_Chart_Data_5min", stockResponse.getCompany()));
            stockResponse.set15MinChart(getChart(statement, "Stock_To_Chart_Data_15min", stockResponse.getCompany()));
        }
        return stocks;
    }

    private UserResponse buildUserResponse(Statement statement, ResultSet userRs, long userId)
        throws SQLException, DBServiceException {
        UserResponse user = UserResponse.create(userRs);
        user.setFavouriteStocks(getFavouriteStocksForUserId(statement, userId));
        return user;
    }

    @Override
    public Optional<UserResponse> getUserByRegistrationServiceId(String serviceField, String serviceId)
        throws DBServiceException {
        try (Statement statement = connection.createStatement()) {
            ResultSet userRs = statement.executeQuery(
                format("SELECT * FROM Users WHERE %s = '%s'", serviceField, serviceId));
            if (userRs.next()) {
                long userId = userRs.getLong("id");
                return Optional.of(buildUserResponse(statement, userRs, userId));
            } else {
                return Optional.empty();
            }
        } catch (SQLException throwable) {
            throw new DBServiceException(format("Error while finding user with %s = '%s'", serviceField, serviceId));
        }
    }

    @Override
    public long getUserIdByRefreshToken(String refreshToken) throws DBServiceException {
        try (Statement statement = connection.createStatement()) {
            ResultSet userRs = statement.executeQuery(format("SELECT id FROM Users WHERE refresh_token = '%s'", refreshToken));
            if (userRs.next()) {
                return userRs.getLong("id");
            } else {
                throw new DBServiceException(format("User was not matched with refresh token %s", refreshToken));
            }
        } catch (SQLException throwable) {
            throw new DBServiceException(format("Error while getting user with refresh token %s", refreshToken), throwable);
        }
    }

    @Override
    public long addUser(CreateUserRequest request) throws DBServiceException {
        try (Statement statement = connection.createStatement()) {
            String query =
                format("INSERT INTO Users(name, refresh_token, apple_id) VALUES('%s', '%s', '%s') RETURNING id",
                    request.getName(), request.getRefreshToken(), request.getAppleId());
            ResultSet userRs = statement.executeQuery(query);
            if (userRs.next()) {
                return userRs.getLong("id");
            } else {
                throw new DBServiceException(
                    format("User id was not returned after creating. Request: %s", request.toString()));
            }
        } catch (SQLException throwable) {
            throw new DBServiceException(format("Error while creating user %s", request.toString()), throwable);
        }
    }

    private List<ChartEntry> getChart(Statement statement, String table, String company) throws SQLException {
        ResultSet chartRs = statement.executeQuery(
            format("SELECT * FROM %s WHERE stock_name = '%s' ORDER BY time ASC", table, company));
        List<ChartEntry> chart = new ArrayList<>();
        while (chartRs.next()) {
            chart.add(new ChartEntry(
                chartRs.getDouble("open"),
                chartRs.getDouble("close"),
                chartRs.getDouble("low"),
                chartRs.getDouble("high"),
                chartRs.getTimestamp("time")));
        }
        return chart;
    }

    @Override
    public StockResponse getStockOverview(String ticker) throws DBServiceException {
        try (Statement statement = connection.createStatement()) {
            ResultSet stockRs = statement.executeQuery(format("SELECT * FROM Stock_Data WHERE ticker = '%s'", ticker));
            if (stockRs.next()) {
                StockResponse stockResponse = StockResponse.create(stockRs);
                stockResponse.set5MinChart(getChart(statement, "Stock_To_Chart_Data_5min", stockResponse.getCompany()));
                stockResponse.set15MinChart(getChart(statement, "Stock_To_Chart_Data_15min", stockResponse.getCompany()));
                return stockResponse;
            }
            throw new DBServiceException(format("Ticker %s was not found", ticker));
        } catch (SQLException throwable) {
            throw new DBServiceException(format("Error while getting stock %s", ticker), throwable);
        }
    }

    @Override
    public UserResponse getUser(long userId) throws DBServiceException {
        try (Statement statement = connection.createStatement()) {
            ResultSet userRs = statement.executeQuery(format("SELECT * FROM Users WHERE id = %d", userId));
            if (userRs.next()) {
                return buildUserResponse(statement, userRs, userId);
            } else {
                throw new DBServiceException(format("User %d was not found", userId));
            }
        } catch (SQLException throwable) {
            throw new DBServiceException(format("Error while getting user %d", userId), throwable);
        }
    }
}