/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package itb.nlp.gate.crawler.utils;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author asatrya
 */
public class DbConnection {

    private Connection connection = null;

    private String host;
    private int port;
    private String database;
    private String user;
    private String pass;

    public DbConnection() {
        this.host = Configuration.getConfiguration().getDb_host();
        this.port = Configuration.getConfiguration().getDb_port();
        this.database = Configuration.getConfiguration().getDb_database();
        this.user = Configuration.getConfiguration().getDb_user();
        this.pass = Configuration.getConfiguration().getDb_pass();
    }

    public Connection getConnection(){
       if(connection == null){
            try {
                Class.forName("com.mysql.jdbc.Driver").newInstance();
                String connectionURL = "jdbc:mysql://" + host + ":" + port + "/" + database;
                connection = DriverManager.getConnection(connectionURL, user, "");
            } catch (SQLException ex) {
                Logger.getLogger(DbConnection.class.getName()).log(Level.SEVERE, null, ex);
            } catch (ClassNotFoundException ex) {
                Logger.getLogger(DbConnection.class.getName()).log(Level.SEVERE, null, ex);
            } catch (InstantiationException ex) {
                Logger.getLogger(DbConnection.class.getName()).log(Level.SEVERE, null, ex);
            } catch (IllegalAccessException ex) {
                Logger.getLogger(DbConnection.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        return connection;
    }

    public void closeConnection(){
        if(connection != null){
            try {
                connection.close();
            } catch (SQLException ex) {
                Logger.getLogger(DbConnection.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
}
