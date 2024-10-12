package com.latex2nemeth.parser.aux;

import org.junit.Test;

import static junit.framework.TestCase.assertEquals;

/**
 * Created by aggelgian on 17/10/2015.
 */
public class LabelTableTest {

    @Test
    public void testCreateLabels() {
        LabelTable labelTable = new LabelTable();
        LabelTable expectedLabelTable = new LabelTable();

        // Parse the aux files.
        String auxFile = this.getClass().getResource("mathtest.aux").getFile();
        labelTable.createlabels(auxFile);
        // Generate the expected map.
	// Deleted by andpapas
        // expectedLabelTable.put("god", "0.0.1");
        // Validate the map.
        assertEquals(expectedLabelTable, labelTable);
    }
}
