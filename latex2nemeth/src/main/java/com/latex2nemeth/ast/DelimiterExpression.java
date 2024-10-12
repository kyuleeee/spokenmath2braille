package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;

public class DelimiterExpression extends Expression {
    // TODO: Should these be just Strings?
    private String left, right;
    private Expression content;

    public DelimiterExpression(String left, String right, Expression content, NemethTable table) {
        super(table);
        this.left = left;
        this.right = right;
        this.content = content;
    }

    @Override
    public void assignFractionLevel() {
        // TODO Auto-generated method stub
    }

    @Override
    public void assignOtherLevels() {
        // TODO Auto-generated method stub
    }

    @Override
    public String getBraille() {
        String leftcode = "", rightcode = "";
        String contentString = content.getBraille();

        if (!left.equals("."))
            leftcode = table.getMathCode(left);
        if (!right.equals("."))
            rightcode = table.getMathCode(right);

        if (content instanceof Array ||
                content instanceof MathExpression &&
                        ((MathExpression) content).getChild(0) instanceof Array) {
            contentString = contentString.replaceAll("^\n", "");
            contentString = contentString.replaceAll(" \n$", "");
            contentString = contentString.replaceAll(" \n", "\u2820" + rightcode + "\n\u2820" + leftcode);
            contentString = contentString.replaceAll("^", "\n\u2820" + leftcode);
            contentString = contentString.replaceAll("$", "\u2820" + rightcode + "\n");
        } else {
            contentString = "\u2820" + leftcode + contentString + "\u2820" + rightcode;
        }
        return contentString;
    }

	
}
