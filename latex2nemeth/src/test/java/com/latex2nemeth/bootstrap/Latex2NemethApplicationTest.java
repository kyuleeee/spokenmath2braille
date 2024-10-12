package com.latex2nemeth.bootstrap;

import com.latex2nemeth.parser.ParseException;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.FilenameUtils;
import org.apache.commons.io.IOUtils;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;

import static junit.framework.TestCase.assertEquals;

public class Latex2NemethApplicationTest {

    @Rule
    public TemporaryFolder folder = new TemporaryFolder();

    private Logger logger = LoggerFactory.getLogger(Latex2NemethApplicationTest.class);

    @Test
    public void testSimple() throws IOException, ParseException {
        String prefix = "mathtest";
        String encodingFile = this.getClass().getResource("nemeth.json").getFile();
        String texFile = this.getClass().getResource(prefix + ".tex").getFile();
        String auxFile = this.getClass().getResource(prefix + ".aux").getFile();
        String folderPath = folder.getRoot().getCanonicalPath();

        // Generate the nemeth files.
        String[] args = {texFile, auxFile, Latex2NemethApplication.getOutCliOption(),
                FilenameUtils.concat(folderPath, prefix), Latex2NemethApplication.getEncodingCliOption(),
                FilenameUtils.concat(folderPath, encodingFile)};
        Latex2NemethApplication.main(args);

        // Validate each chapter.
        for (int i = 0; i < 5; i++) {
            // Load expected output.
            String filename = prefix + i + ".nemeth";
            InputStream inputStream = this.getClass().getResourceAsStream(filename);
            String expectedContent = IOUtils.toString(inputStream, "UTF-8");

            // Load actual output.
            String generatedFilename = FilenameUtils.concat(folderPath, filename);
            File file = new File(generatedFilename);
            String content = FileUtils.readFileToString(file, "UTF-8");

            // and compare.
            assertEquals(expectedContent, content);
        }
    }
}
