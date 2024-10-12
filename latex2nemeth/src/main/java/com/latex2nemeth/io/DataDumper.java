package com.latex2nemeth.io;

import com.latex2nemeth.parser.aux.ParsedChapters;
import org.daisy.braille.api.factory.FactoryProperties;
import org.daisy.braille.consumer.table.TableCatalog;
import org.daisy.braille.pef.TextConverterFacade;
import org.daisy.cli.ShortFormResolver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

public class DataDumper {

    public enum OutputMode {
        NEMETH, PEF
    }

    private OutputMode outputMode;
    private ParsedChapters parsedChapters;
    private String baseFilename;
    private ShortFormResolver shortFormResolver;

    private static Logger logger = LoggerFactory.getLogger(DataDumper.class);

    public DataDumper(String selectedOutputMode) {
        // Set the output mode.
        switch (selectedOutputMode.toLowerCase()){
            case "pef":
                outputMode = OutputMode.PEF;
                break;
            case "nemeth":
            default:
                outputMode = OutputMode.NEMETH;
                break;
        }

        // Initialize the shortFormResolver, if needed.
        if (outputMode == OutputMode.PEF) {
            TableCatalog tableCatalog = TableCatalog.newInstance();
            Collection<String> idents = new ArrayList<>();
            for (FactoryProperties p : tableCatalog.list()) { idents.add(p.getIdentifier()); }
            shortFormResolver = new ShortFormResolver(idents);
        }
    }

    public void setParsedChapters(ParsedChapters parsedChapters) {
        this.parsedChapters = parsedChapters;
    }

    public void setBaseFilename(String baseFilename) {
        this.baseFilename = baseFilename;
    }

    /**
     * Dump the parsed Braille chapters to files.
     * @throws IOException
     */
    public void dumpParsedChaptersToFiles() throws IOException {
        // Create a file for each chapter.
        for (Map.Entry<Integer, String> chapterEntry : parsedChapters.entrySet()) {
            switch (outputMode) {
                case NEMETH:
                    writeStringToNemethFile(chapterEntry.getKey(), chapterEntry.getValue());
                    break;
                case PEF:
                    writeStringToPefFile(chapterEntry.getKey(), chapterEntry.getValue());
                    break;
            }
        }
    }

    /**
     * Write the parsed Braille chapter to a nemeth file.
     * @param chapter the number of the chapter.
     * @param data the contents of the chapter.
     * @throws IOException
     */
    private void writeStringToNemethFile(int chapter, String data) throws IOException {
        String filename = baseFilename + chapter + ".nemeth";
        logger.info("Creating " + filename);
        Writer output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(filename), "UTF-16"));
        output.write(data);
        output.flush();
        output.close();
    }

    public static void writePicture(int i, String data) {
        String filename = "picture" + i + ".tex";
        try {
            logger.info("Creating " + filename);
            Writer output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(filename), "UTF-16"));
            output.write(data);
            output.flush();
            output.close();
        } catch (Exception e) {
            logger.info("Could not create " + filename);
        }
    }

    /**
     * Write the parsed Braille chapter to a pef file.
     * @param chapter the number of the chapter.
     * @param data the contents of the chapter.
     * @throws IOException
     */
    private void writeStringToPefFile(int chapter, String data) throws IOException {
        String filename = baseFilename + chapter + ".pef";
        File tempFile = File.createTempFile(baseFilename + chapter, ".tmp");
        String tempFilePath = tempFile.getCanonicalPath();

        // Create the temporary unicode file.
        Writer output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(tempFilePath), "UTF-8"));
        output.write(data.replaceAll(" ", "\u2800"));
        output.flush();
        output.close();

        // Convert the unicode file to PEF format.
        logger.info("Creating " + filename);
        Map<String, String> opts = new HashMap<>();
        opts.put(TextConverterFacade.KEY_MODE, shortFormResolver.resolve("unicode_braille"));

        File input = new File(tempFile.getCanonicalPath());
        File pefOutput = new File(filename);
        new TextConverterFacade(TableCatalog.newInstance()).parseTextFile(input, pefOutput, opts);

        // Delete the temporary file.
        tempFile.delete();
    }
}
