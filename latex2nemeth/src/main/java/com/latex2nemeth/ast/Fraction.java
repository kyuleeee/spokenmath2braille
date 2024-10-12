package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;

public class Fraction extends Expression {

    protected Expression numerator, denominator;

    public Fraction(Expression num, Expression denom, NemethTable table) {
        super(table);
        this.numerator = num;
        this.denominator = denom;
//		this.fractionlevel = 1 + Math.max(numerator.fractionlevel, denominator.fractionlevel);
    }

    @Override
    public void assignFractionLevel() {
        numerator.assignFractionLevel();
        denominator.assignFractionLevel();
        fractionlevel = 1 + Math.max(numerator.fractionlevel, denominator.fractionlevel);
    }

    @Override
    public void assignOtherLevels() {
       numerator.assignOtherLevels();
       denominator.assignOtherLevels();
    }

    @Override
    public String getBraille() {
        StringBuffer buffer = new StringBuffer();
        String level = table.getMathCode("frac-level");
        String begin = table.getMathCode("\\frac-b");
        String end = table.getMathCode("\\frac-e");
        String sep = table.getMathCode("/");

        for (int i = 0; i < fractionlevel - 1; i++) {
            buffer.append(level);
        }
        buffer.append(begin);
        buffer.append(numerator.getBraille());
        for (int i = 0; i < fractionlevel - 1; i++) {
            buffer.append(level);
        }
        buffer.append(sep);
        buffer.append(denominator.getBraille());
        for (int i = 0; i < fractionlevel - 1; i++) {
            buffer.append(level);
        }
        buffer.append(end);
        return buffer.toString();
    }

    
}
