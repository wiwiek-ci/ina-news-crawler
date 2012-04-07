/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package itb.nlp.gate.crawler.utils;

import gate.Document;
import gate.Factory;
import gate.FeatureMap;
import gate.creole.ResourceInstantiationException;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author asatrya
 */
public class DocumentHelper {

    private FeatureMap params;
    private FeatureMap features;
    private Document document;
    private File file;

    public DocumentHelper(FeatureMap params, FeatureMap features) {
        this.params = params;
        this.features = features;
        this.document = createDocument();
        this.document.setFeatures(features);
    }

    private Document createDocument(){
        Document doc = null;
        try {
            doc = (Document) Factory.createResource("gate.corpora.DocumentImpl", params);
        } catch (ResourceInstantiationException ex) {
            Logger.getLogger(DocumentHelper.class.getName()).log(Level.SEVERE, null, ex);
        }
        return doc;
    }

    public Document getDocument() {
        return document;
    }

    public File getFile() {
        return file;
    }

    public void save(){
        Writer output = null;
        try {
            Date fetchedDate = new Date(((Timestamp)this.features.get("fetched_at")).getTime());
            SimpleDateFormat year = new SimpleDateFormat("yyyy");
            SimpleDateFormat month = new SimpleDateFormat("MM");
            SimpleDateFormat day = new SimpleDateFormat("dd");
            File parentDir = new File(Configuration.getConfiguration().getFiles_path());
            if(! parentDir.exists()){
                parentDir.mkdirs();
            }
            File dir = new File(
                    parentDir,
                    year.format(fetchedDate) + File.separator + month.format(fetchedDate) + File.separator + day.format(fetchedDate));
            if (!dir.exists()) {
                dir.mkdirs();
            }
            file = new File(dir, this.features.get("category").toString() + "_" + this.features.get("id").toString() + ".xml");
            output = new BufferedWriter(new FileWriter(file));
            output.write(getDocument().toXml());
            output.close();
        } catch (IOException ex) {
            Logger.getLogger(DocumentHelper.class.getName()).log(Level.SEVERE, null, ex);
        } finally {
            try {
                output.close();
            } catch (IOException ex) {
                Logger.getLogger(DocumentHelper.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

}
