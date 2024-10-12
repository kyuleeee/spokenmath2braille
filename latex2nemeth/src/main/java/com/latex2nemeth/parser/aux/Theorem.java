package com.latex2nemeth.parser.aux;

public class Theorem {

    private String name;
    private String label;
    private int counter;
    private Theorem counterTheorem;
    private int tokenNumber;

    public Theorem(String name, String label) {
        this.name = name;
        this.label = label;
        counterTheorem = this;
        resetCounter();
    }

    public Theorem(String name, String label, Theorem counterTheorem) {
        this(name,label);
        this.counterTheorem = counterTheorem;
    }

    public String getLabel() {
        return label;
    }

    public void resetCounter() {
        counter = 0;
    }

    public int getNextCounter() {
        return ++counterTheorem.counter;
    }
}