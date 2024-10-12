package com.latex2nemeth.bootstrap;

import com.latex2nemeth.io.DataDumper;
import com.latex2nemeth.parser.Latex;
import com.latex2nemeth.parser.ParseException;
import com.latex2nemeth.parser.aux.ParsedChapters;
import com.latex2nemeth.symbols.NemethTable;
import com.latex2nemeth.utils.Preamble;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.MissingOptionException;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.io.FilenameUtils;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;


public class Latex2NemethApplication {

    private static final String OPT_OUT_PREFIX = "o";
    private static final String OPT_OUT_MODE = "m";
    private static final String OPT_OUT_MODE_LONG = "mode";
    private static final String OPT_ENC_TABLE = "e";
    private static final String OPT_ENC_TABLE_LONG = "encoding";
    private static final String OPT_VERBOSE = "v";
    private static final String OPT_VERBOSE_LONG = "verbose";

    private static final String DEFAULT_ENCODING_TABLE = "/encoding/nemeth.json";

    private static Logger logger = LoggerFactory.getLogger(Latex2NemethApplication.class);

    public static void main(String[] args) throws IOException, ParseException {

        // Build the CLI options.
        Options options = buildOptions();
        try {
            // Parse the CLI arguments.
            CommandLineParser parser = new DefaultParser();
            CommandLine cmd = parser.parse(options, args);
            String[] arguments = cmd.getArgs();
            if (arguments.length < 2) {
                printUsage(options);
                System.exit(1);
            }
            String texFile = arguments[0];
            String auxFile = arguments[1];
            String texBaseFilename = FilenameUtils.getBaseName(texFile);
            String baseFilename = FilenameUtils.normalize(cmd.getOptionValue(OPT_OUT_PREFIX, texBaseFilename));
            
            // Set the encoding table.
            // String encodingTableFile = FilenameUtils.normalize(cmd.getOptionValue(OPT_ENC_TABLE, DEFAULT_ENCODING_TABLE));
            String encodingTableFile = cmd.getOptionValue(OPT_ENC_TABLE, DEFAULT_ENCODING_TABLE);
            boolean isLocalResource = StringUtils.equals(encodingTableFile, DEFAULT_ENCODING_TABLE);
            NemethTable encodingTable = new NemethTable(encodingTableFile, isLocalResource);

            boolean verbose = cmd.hasOption(OPT_VERBOSE);

            // Invoke the parser and get the chapters.
            ParsedChapters chapters = Latex.parse(texFile, auxFile, encodingTable, new Preamble(), verbose);


            // Dump the chapters to files.
            DataDumper dataDumper = new DataDumper(cmd.getOptionValue(OPT_OUT_MODE, ""));
            dataDumper.setBaseFilename(baseFilename);
            dataDumper.setParsedChapters(chapters);
            dataDumper.dumpParsedChaptersToFiles();

        } 
        catch (org.apache.commons.cli.MissingOptionException e) {
            System.err.println("[ERROR] " + e.getMessage());
            printUsage(options);
        } 
        catch (org.apache.commons.cli.ParseException e) {
            System.err.println("Unexpected exception: " + e.getMessage());
        }
//        catch (StopExecutionException e) {
//            System.err.println("Exception occured: " + e.getMessage());
//        }
    }

    /**
     * Generate the CLI options.
     * @return options generated.
     */
    private static Options buildOptions() {
        Options options = new Options();
        // Add the option for the output file(s).
        Option outOpt = new Option(OPT_OUT_PREFIX, true, "The output prefix of the Braille files. " +
                "It can also be prefixed with a path to a specific directory.\n" +
                "The default value is the name of the TeX file.");
        options.addOption(outOpt);
        // Add the option for the mode.
        Option mOpt = new Option(OPT_OUT_MODE, OPT_OUT_MODE_LONG, true, "The mode of the parser which controls " +
                "the type of the output Braille files.\n" +
                "It can be either nemeth or pef. The default mode is nemeth.");
        options.addOption(mOpt);
        // Add the option for the encoding table.
        Option eOpt = new Option(OPT_ENC_TABLE, OPT_ENC_TABLE_LONG, true, "The encoding table for Braille " +
                "in the form of a JSON file.\n" +
                "If not specified, Nemeth encoding will be used.");
        options.addOption(eOpt);
        
        Option verbose = new Option(OPT_VERBOSE, OPT_VERBOSE_LONG, false, "Print verbose output.");
        
        options.addOption(verbose);

        return options;
    }

    /**
     * Print the usage message.
     * @param options the CLI options.
     */
    private static void printUsage(Options options) {
        String header = "\nOptions:\n";
        String footer = "\nPlease report issues to andpapas@aegean.gr";

        HelpFormatter formatter = new HelpFormatter();
        formatter.printHelp("usage: java -jar latex2nemeth.jar [options] texFile auxFile",
                header, options, footer, false);
    }

    /**
     * Returns the CLI option for the prefix for output files.
     * @return the minus prefixed option.
     */
    public static String getOutCliOption() {
        return "-" + OPT_OUT_PREFIX;
    }

    /**
     * Return the CLI option for selecting an encoding file.
     * @return the minus prefixed option.
     */
    public static String getEncodingCliOption() { return "-" + OPT_ENC_TABLE; }
}
