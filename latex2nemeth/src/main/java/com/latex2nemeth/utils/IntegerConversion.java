package com.latex2nemeth.utils;

public class IntegerConversion {

    /**
     * Convert an integer to a Greek numeral.
     * TODO Works for numbers 1 to 9999.
     *
     * @param input the integer to convert.
     * @return the Greek numeral as a string.
     */
    public static String integerToGreek(int input) {
        String digits[][] = {
                {"", "α", "β", "γ", "δ", "ε", "στ", "ζ", "η", "θ"},
                {"", "ι", "κ", "λ", "μ", "ν", "ξ", "ο", "π", "q"},
                {"", "ρ", "σ", "τ", "υ", "φ", "χ", "ψ", "ω", "t"},
                {"", "α", "β", "γ", "δ", "ε", "στ", "ζ", "η", "θ"}
        };
        String s = "";
        int d, pos = 0;
        while (input != 0) {
            d = input % 10;
            s = digits[pos++][d] + s;
            input /= 10;
        }
        return s;
    }

    /**
     * Convert an integer to a Roman numeral.
     * TODO Works for integers up to 3999.
     *
     * @param input the integer to convert.
     * @return the Roman numeral as a string.
     * @url http://stackoverflow.com/questions/12967896/converting-integers-to-roman-numerals-java
     */
    public static String integerToRomanNumeral(int input) {
        if (input < 1 || input > 3999)
            return "Invalid Roman Number Value";
        String s = "";
        while (input >= 1000) {
            s += "M";
            input -= 1000;
        }
        while (input >= 900) {
            s += "CM";
            input -= 900;
        }
        while (input >= 500) {
            s += "D";
            input -= 500;
        }
        while (input >= 400) {
            s += "CD";
            input -= 400;
        }
        while (input >= 100) {
            s += "C";
            input -= 100;
        }
        while (input >= 90) {
            s += "XC";
            input -= 90;
        }
        while (input >= 50) {
            s += "L";
            input -= 50;
        }
        while (input >= 40) {
            s += "XL";
            input -= 40;
        }
        while (input >= 10) {
            s += "X";
            input -= 10;
        }
        while (input >= 9) {
            s += "IX";
            input -= 9;
        }
        while (input >= 5) {
            s += "V";
            input -= 5;
        }
        while (input >= 4) {
            s += "IV";
            input -= 4;
        }
        while (input >= 1) {
            s += "I";
            input -= 1;
        }
        return s;
    }
}
