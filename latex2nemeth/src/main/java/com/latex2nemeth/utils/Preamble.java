package com.latex2nemeth.utils;

/**
 * Created by aggelgian on 17/5/2016.
 */
public class Preamble {

    private String start;
    private String end;

    public Preamble() {
        this.start = "\\documentclass{article}\n" +
                "\\usepackage{pstricks}\n"+
                "\\begin{document}\n";
        this.end = "\n\\end{document}\n";
    }

    public Preamble(String start, String end) {
        this.start = start;
        this.end = end;
    }

    public String getStart() {
        return start;
    }

    public void setStart(String start) {
        this.start = start;
    }

    public String getEnd() {
        return end;
    }

    public void setEnd(String end) {
        this.end = end;
    }

    @Override
    public String toString() {
        final StringBuilder sb = new StringBuilder("Preamble{");
        sb.append("start='").append(start).append('\'');
        sb.append(", end='").append(end).append('\'');
        sb.append('}');
        return sb.toString();
    }
}
