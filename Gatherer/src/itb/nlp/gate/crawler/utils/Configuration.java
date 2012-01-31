/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package itb.nlp.gate.crawler.utils;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author asatrya
 */
public class Configuration {
    private static Configuration configuration = null;

    private String db_host = "localhost";
    private int db_port = 3360;
    private String db_database = "crawler";
    private String db_user = "root";
    private String db_pass = "";
    private String files_path = "";
    private int rows_fetched_each = 10;
    private int delay = 5000;

    private Configuration(){
        FileInputStream fstream = null;
        try {
            fstream = new FileInputStream("gatherer.conf");
            DataInputStream input = new DataInputStream(fstream);
            BufferedReader reader = new BufferedReader(new InputStreamReader(input));
            String strLine = "";
            while((strLine = reader.readLine()) != null){
                if (!strLine.equals("") && strLine.charAt(0) != '#') {
                    String[] line = strLine.split("=");
                    String param = line[0].trim();
                    String value = "";
                    if(line.length >= 2){
                        value = line[1].trim();
                    }

                    if("db_host".equalsIgnoreCase(param)){
                        db_host = value;
                    }
                    if("db_port".equalsIgnoreCase(param)){
                        db_port = Integer.parseInt(value);
                    }
                    if("db_database".equalsIgnoreCase(param)){
                        db_database = value;
                    }
                    if("db_user".equalsIgnoreCase(param)){
                        db_user = value;
                    }
                    if("files_path".equalsIgnoreCase(param)){
                        files_path = value;
                    }
                    if("rows_fetched_each".equalsIgnoreCase(param)){
                        rows_fetched_each = Integer.parseInt(value);
                    }
                    if("delay".equalsIgnoreCase(param)){
                        delay = Integer.parseInt(value);
                    }
                }
            }
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Configuration.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(Configuration.class.getName()).log(Level.SEVERE, null, ex);
        } finally {
            try {
                fstream.close();
            } catch (IOException ex) {
                Logger.getLogger(Configuration.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    public static Configuration getConfiguration(){
        if(configuration == null){
            configuration = new Configuration();
        }
        return configuration;
    }

    public String getDb_database() {
        return db_database;
    }

    public String getDb_host() {
        return db_host;
    }

    public String getDb_pass() {
        return db_pass;
    }

    public int getDb_port() {
        return db_port;
    }

    public String getDb_user() {
        return db_user;
    }

    public String getFiles_path() {
        return files_path;
    }

    public int getRows_fetched_each() {
        return rows_fetched_each;
    }

    public int getDelay() {
        return delay;
    }

    @Override
    public String toString(){
        String str = "Configuration:\n";
        str += "db_host=" + db_host + "\n";
        str += "db_port=" + db_port + "\n";
        str += "db_database=" + db_database + "\n";
        str += "db_user=" + db_user + "\n";
        str += "db_pass=" + db_pass + "\n";
        str += "files_path=" + files_path + "\n";
        str += "rows_fetched_each=" + rows_fetched_each + "\n";
        str += "delay=" + delay + "\n";
        return str;
    }
}
