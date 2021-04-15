package db_service;

import java.util.Optional;

import model.ChangeFavouritesRequest;
import model.CreateUserRequest;
import model.StockResponse;
import model.UserResponse;

public interface DBService {
    void addFavourite(int userId, ChangeFavouritesRequest request) throws DBServiceException;
    void removeFavourite(int userId, ChangeFavouritesRequest request) throws DBServiceException;
    void updateRefreshToken(long userId, String refreshToken) throws DBServiceException;
    Optional<UserResponse> getUserByRegistrationServiceId(String serviceField, String serviceId) throws DBServiceException;
    long getUserIdByRefreshToken(String refreshToken) throws DBServiceException;
    long addUser(CreateUserRequest request) throws DBServiceException;
    StockResponse getStockOverview(String ticker) throws DBServiceException;
    UserResponse getUser(long userId) throws DBServiceException;

}
