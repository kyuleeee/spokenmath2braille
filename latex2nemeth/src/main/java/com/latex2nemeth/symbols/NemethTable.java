package com.latex2nemeth.symbols;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class NemethTable {

    private Map<String, String> letters;
    private Map<String, String> mathSymbols;
    private Map<String, String> theoremSymbols;

    private static Logger logger = LoggerFactory.getLogger(NemethTable.class);

    public NemethTable(String filename, boolean isLocalResource) {
        // Load the encoding table.
        JSONObject rootObj = loadTableFromJson(filename, isLocalResource);
        JSONObject lettersObj = (JSONObject) rootObj.get("letters");
        JSONObject mathSymbolsObj = (JSONObject) rootObj.get("mathSymbols");
        JSONObject theoremSymbolsObj = (JSONObject) rootObj.get("theoremSymbols");
        letters = loadFromJsonObj(lettersObj);
        mathSymbols = loadFromJsonObj(mathSymbolsObj);
        theoremSymbols = loadFromJsonObj(theoremSymbolsObj);
    }

    private JSONObject loadTableFromJson(String filename, boolean isLocalResource) {
        JSONParser parser = new JSONParser();
        try {
            BufferedReader reader;
            if (isLocalResource) {
                reader = new BufferedReader(new InputStreamReader(this.getClass().getResourceAsStream(filename)));
            } else {
                reader = new BufferedReader(new FileReader(filename));
            }
            return (JSONObject) parser.parse(reader);
        } catch (Exception e) {
            String message = "Could not load the encoding table from " + filename;
            logger.error(message, e);
            return new JSONObject(new HashMap()); // Will fail.
        }
    }

    public String getLetterCode(String key) {
        return letters.get(key);
    }

    public String getMathCode(String key) {
        return mathSymbols.get(key);
    }

    public String getTheoremCode(String key) {
        return theoremSymbols.get(key);
    }

    private Map<String, String> loadFromJsonObj(JSONObject obj) {
        Map<String, String> hashMap = new HashMap<>();
        Set<String> keys = obj.keySet();
        for (String key : keys) {
            String value = (String) obj.get(key);
            hashMap.put(key, value);
        }
        return hashMap;
    }
}
