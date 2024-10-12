package com.latex2nemeth.ast;


import com.latex2nemeth.symbols.NemethTable;

public class Sqrt extends Expression {
    private Expression root;
    private Expression order;
    
    public Sqrt(Expression root, NemethTable table) {
        super(table);
        this.root = root;
    }

    public Sqrt(Expression root, Expression order, NemethTable table) {
        this(root, table);
        this.order = order;
    }

    @Override
    public void assignFractionLevel() {
        root.assignFractionLevel();
        this.fractionlevel = root.fractionlevel;
    }

    @Override
    public void assignOtherLevels() {
        root.sublevel = this.sublevel;
        root.suplevel = this.suplevel;
        root.sqrtlevel = this.sqrtlevel + 1;
        root.assignOtherLevels();
    }

    @Override
    public String getBraille() {
        // Page 111
        StringBuffer buffer = new StringBuffer();
        String nemLevel = table.getMathCode("\\sqrt-level");
        String sqrt_b = table.getMathCode("\\sqrt-b");
        String sqrt_e = table.getMathCode("\\sqrt-e");
        String radical_index = table.getMathCode("\\radical-index");

        if (order != null) {
            buffer.append(radical_index);
            // What about number indicators in math mode.
//			buffer.append(table.getMathCode("NS"));
            buffer.append(order.getBraille());
        }

        for (int i = 0; i < sqrtlevel; i++) {
            buffer.append(nemLevel);
        }
        buffer.append(sqrt_b);
        buffer.append(root.getBraille());
        for (int i = 0; i < sqrtlevel; i++) {
            buffer.append(nemLevel);
        }
        buffer.append(sqrt_e);

        return buffer.toString();
    }

    
}
