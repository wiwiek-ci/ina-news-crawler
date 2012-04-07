/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package itb.nlp.gate.crawler;

import gate.Document;
import gate.Factory;
import gate.FeatureMap;
import gate.Gate;
import gate.util.GateException;
import itb.nlp.gate.crawler.models.Article;
import itb.nlp.gate.crawler.utils.Configuration;
import itb.nlp.gate.crawler.utils.DbConnection;
import itb.nlp.gate.crawler.utils.DocumentHelper;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author asatrya
 */
public class Gatherer {
    public static void main(String[] args){
        DbConnection dbCon = null;
        try {
            // GATE initialization
            Gate.init();

            // Database initialization
            dbCon = new DbConnection();
            Article articleModel = new Article(dbCon.getConnection());

            // Print to console
            System.out.println("Gatherer is running (Press Ctrl+C to stop)");
            System.out.println(Configuration.getConfiguration().toString());

            while (true) {
                // Fetch data
                ResultSet resultSet = articleModel.fetchArticles();

                // For each record in resultSet, do:
                // - Get data
                // - Set is_gathered flag = 1
                // - Create corresponding GATE document
                while (resultSet != null && resultSet.next()) {
                    // Get data for each record
                    int id = resultSet.getInt(1);
                    String source = resultSet.getString(2);
                    String url = resultSet.getString(3);
                    String category = resultSet.getString(4);
                    String title = resultSet.getString(5);
                    String subtitle = resultSet.getString(6);
                    String content = resultSet.getString(7);
                    //Timestamp published_at = resultSet.getTimestamp(8);
                    String place = resultSet.getString(9);
                    String author = resultSet.getString(10);
                    Timestamp fetched_at = resultSet.getTimestamp(11);

                    // Set is_gathered flag = 1
                    articleModel.setArticleAsGathered(id);

                    // Create GATE Document
                    FeatureMap params = Factory.newFeatureMap();
                    params.put(Document.DOCUMENT_ENCODING_PARAMETER_NAME, "UTF-8");
                    params.put(Document.DOCUMENT_MARKUP_AWARE_PARAMETER_NAME, false);
                    params.put(Document.DOCUMENT_STRING_CONTENT_PARAMETER_NAME, title + "\n"
                            + subtitle + "\n" + content);

                    FeatureMap features = Factory.newFeatureMap();
                    features.put("id", id);
                    features.put("source", source);
                    features.put("url", url);
                    features.put("category", category);
                    features.put("title", title);
                    features.put("subtitle", subtitle);
                    //features.put("published_at", published_at);
                    //features.put("published_at_str", published_at.toString());
                    features.put("fetched_at", fetched_at);
                    features.put("fetched_at_str", fetched_at.toString());
                    features.put("place", place);
                    features.put("author", author);

                    DocumentHelper documentHelper = new DocumentHelper(params, features);
                    documentHelper.save();

                    // Print info to console
                    System.out.println("Save doc " + id + " to " + documentHelper.getFile().getAbsolutePath());
                }

                Thread.sleep(Configuration.getConfiguration().getDelay());
            }

        } catch (InterruptedException ex) {
            Logger.getLogger(Gatherer.class.getName()).log(Level.SEVERE, null, ex);
        } catch (GateException ex) {
            Logger.getLogger(Gatherer.class.getName()).log(Level.SEVERE, null, ex);
        } catch (SQLException ex) {
            Logger.getLogger(Gatherer.class.getName()).log(Level.SEVERE, null, ex);
        } finally{
            if(dbCon != null){
                dbCon.closeConnection();
            }
        }
    }

}
