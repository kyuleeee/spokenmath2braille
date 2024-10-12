package com.latex2nemeth.parser.aux;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LabelTable extends HashMap<String, String> {

    private static Logger logger = LoggerFactory.getLogger(LabelTable.class);

    public LabelTable() {
        super();
    }

    /**
     * Parse an AUX file and find the labels.
     * @param filename the path of the AUX file
     */
    public void createlabels(String filename) {
        try (FileReader fileReader = new FileReader(filename);
             BufferedReader bufferedReader = new BufferedReader(fileReader)) {
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                Pattern p = Pattern.compile("newlabel\\{([^\\}]*)\\}\\{\\{([0-9\\.]+)\\}\\{[0-9]+\\}\\}");
                Matcher m = p.matcher(line);
                while (m.find()) {
                    this.put(m.group(1), m.group(2));
                }
            }
        } catch (IOException e) {
            logger.error("Error while creating labels", e);
        }
    }
}
