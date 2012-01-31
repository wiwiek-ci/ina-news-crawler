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
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author asatrya
 */
public class Gatherer {
    public static void main(String[] args){
        try {
            // GATE initialization
            Gate.init();

            // Database initilization
            Class.forName("com.mysql.jdbc.Driver").newInstance();
            String connectionURL = "jdbc:mysql://localhost:3306/akademik_crawler";
            Connection connection = DriverManager.getConnection (connectionURL, "root", "");
            Statement selectStatement = connection.createStatement();
            Statement updateStatement = connection.createStatement();

            // Fetch data from database
            String fetchQuery = "SELECT id, source, url, category, title, subtitle, content, "
                    + "published_at, place, author "
                    + "FROM article "
                    + "WHERE is_gathered = 0 "
                    + "ORDER BY id ASC "
                    + "LIMIT 1";
            ResultSet resultSet = selectStatement.executeQuery(fetchQuery);

            // For each record in resultSet, do:
            // - Get data
            // - Set is_gathered flag = 1
            // - Create corresponding GATE document
            while(resultSet.next()){
                // Get data for each record
                int id = resultSet.getInt(1);
                String source = resultSet.getString(2);
                String url = resultSet.getString(3);
                String category = resultSet.getString(4);
                String title = resultSet.getString(5);
                String subtitle = resultSet.getString(6);
                String content = resultSet.getString(7);
                Timestamp published_at = resultSet.getTimestamp(8);
                String place = resultSet.getString(9);
                String author = resultSet.getString(10);

                // Set is_gathered flag = 1
                String updateQuery = "UPDATE article SET is_gathered = 1 WHERE id = " + id;
                updateStatement.executeUpdate(updateQuery);

                // Create GATE Document
                FeatureMap params = Factory.newFeatureMap();
                params.put(Document.DOCUMENT_ENCODING_PARAMETER_NAME, "UTF-8");
                params.put(Document.DOCUMENT_MARKUP_AWARE_PARAMETER_NAME, false);
                params.put(Document.DOCUMENT_STRING_CONTENT_PARAMETER_NAME, title + "\n" +
                        subtitle + "\n" + content);

                Document doc = (Document) Factory.createResource("gate.corpora.DocumentImpl", params);

                FeatureMap attr = Factory.newFeatureMap();
                attr.put("id", id);
                attr.put("source", source);
                attr.put("url", url);
                attr.put("category", category);
                attr.put("title", title);
                attr.put("subtitle", subtitle);
                attr.put("published_at", published_at);
                attr.put("place", place);
                attr.put("author", author);
                doc.setFeatures(attr);

                // Save GATE Document
                Date publishedDate = new Date(published_at.getTime());
                SimpleDateFormat year = new SimpleDateFormat("yyyy");
                SimpleDateFormat month = new SimpleDateFormat("MM");
                File dir = new File(category + File.separator + year.format(publishedDate) +
                        File.separator + month.format(publishedDate));
                if(! dir.exists()){
                    dir.mkdirs();
                }
                File file = new File(dir, id + ".xml");
                Writer output = new BufferedWriter(new FileWriter(file));
                output.write(doc.toXml());
                output.close();

                // Print info to console
                System.out.println("Save doc " + id + " to " + file.getAbsolutePath());
            }

            // Save

        } catch (GateException ex) {
            Logger.getLogger(Gatherer.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(Gatherer.class.getName()).log(Level.SEVERE, null, ex);
        }catch (SQLException ex) {
            Logger.getLogger(Gatherer.class.getName()).log(Level.SEVERE, null, ex);
        } catch (InstantiationException ex) {
            Logger.getLogger(Gatherer.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IllegalAccessException ex) {
            Logger.getLogger(Gatherer.class.getName()).log(Level.SEVERE, null, ex);
        } catch (ClassNotFoundException ex) {
            Logger.getLogger(Gatherer.class.getName()).log(Level.SEVERE, null, ex);
        } 
    }

}
