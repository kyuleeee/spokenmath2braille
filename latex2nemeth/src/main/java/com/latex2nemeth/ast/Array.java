package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;

import java.util.Vector;
import java.util.ArrayList;

public class Array extends Expression {
    private Vector<Expression[]> rows;
    private Vector<Expression> currentRow;
    private String ematrix[][];
    private int nrows, ncols;
    public Array(Vector<Expression[]> ar, NemethTable table) {
        super(table);
        rows = ar;
    }

    public void addExpression(Expression e) {
//    	if (e instanceof Array.Hdotsfor) {
//    		// TODO fill
//    	}
        currentRow.add(e);
    }

    @Override
    public void assignFractionLevel() {
        for (Expression[] r : rows) {
            for (int j = 0; j < ncols; j++) {
                if (r[j] != null)
                    r[j].assignFractionLevel();
            }
        }
    }

    @Override
    public void assignOtherLevels() {
        int i = 0;
        for (Expression[] r : rows) {
            for (int j = 0; j < ncols; j++) {
                if (r[j] != null) {
                    r[j].supsub = new ArrayList<>(this.supsub);
                    r[j].assignOtherLevels();
                }
            }
            i++;
        }
    }

    @Override
    public String getBraille() {
        StringBuffer buffer;
        createMatrix();
        int i, j;
        int colwidths[] = new int[ncols]; // Initialized to 0.

        for (j = 0; j < ncols; j++) {
            for (i = 0; i < nrows; i++) {
                String sexp = ematrix[i][j];
                if (sexp != null && colwidths[j] < sexp.length())
                    colwidths[j] = sexp.length();
            }
        }

        buffer = new StringBuffer();
        buffer.append("\n");
        for (i = 0; i < nrows; i++) {
        	int  nncols = rows.elementAt(i).length;
            for (j = 0; j < nncols; j++) {
            	// Handle hdotosfor
            	Expression[] row = rows.elementAt(i);
            	Expression exp = row[j];
            	if (exp instanceof HdotsforExpression) {
            		HdotsforExpression hexp = (HdotsforExpression) exp;
            		int ncols = hexp.getCols();
            		for (int ll = 1 ; ll <= ncols-1; ll++) {
            			for (int l = 0 ; l <= colwidths[j]; l++) {
            				buffer.append("\u2804"); // dots...
            			}
            			j++;
            		}
            		for (int l = 0 ; l < colwidths[j]; l++) {
        				buffer.append("\u2804"); // dots...
        			}
            		buffer.append(" ");
            	}
            	else {
            		buffer.append(ematrix[i][j]);
            		int spaces = colwidths[j] - ematrix[i][j].length();
            		for (int k = 0; k <= spaces; k++) {
            			buffer.append(" ");
            		}
            	}
            }
            buffer.append("\n");
        }

        return buffer.toString();
    }

    protected void createMatrix() {

        nrows = rows.size();
        ncols=0;
        for (Expression[] r : rows) {
        	if (ncols < r.length) {
        		ncols = r.length;
        	}
        }
  //      ncols = rows.elementAt(0).length;
        
        ematrix = new String[nrows][ncols];
        int i, j;

        i = 0;
        for (Expression[] r : rows) {
        	int nncols = r.length;
            for (j = 0; j < nncols; j++) {
                if (r[j] != null)
                    ematrix[i][j] = r[j].getBraille();
                else
                    ematrix[i][j] = " ";
            }
            i++;
        }
    }

	
}
