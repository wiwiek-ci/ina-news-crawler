/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package itb.nlp.gate.crawler.models;

import itb.nlp.gate.crawler.utils.Configuration;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author asatrya
 */
public class Article {

    private Connection connection = null;

    public Article(Connection connection) {
        this.connection = connection;
    }

    public ResultSet fetchArticles(){
        ResultSet resultSet = null;
        try {
            Statement selectStatement = connection.createStatement();
            // Fetch data from database
            String fetchQuery = "SELECT id, source, url, category, title, subtitle, content, " 
                    + "published_at, place, author "
                    + "FROM article "
                    + "WHERE is_gathered = 0 "
                    + "ORDER BY id ASC "
                    + "LIMIT " + Configuration.getConfiguration().getRows_fetched_each();
            resultSet = selectStatement.executeQuery(fetchQuery);
        } catch (SQLException ex) {
            Logger.getLogger(Article.class.getName()).log(Level.SEVERE, null, ex);
        }
        return resultSet;
    }

    public int setArticleAsGathered(int id){
        int updatedRow = -1;
        try {
            Statement updateStatement = connection.createStatement();
            String updateQuery = "UPDATE article SET is_gathered = 1 WHERE id = " + id;
            updatedRow = updateStatement.executeUpdate(updateQuery);
        } catch (SQLException ex) {
            Logger.getLogger(Article.class.getName()).log(Level.SEVERE, null, ex);
        }
        return updatedRow;
    }

}
