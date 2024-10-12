package com.latex2nemeth.ast;

import com.latex2nemeth.geom.Box;
import com.latex2nemeth.symbols.NemethTable;

import java.util.ArrayList;

public abstract class Expression {
    protected int sqrtlevel = 0;
    protected int sublevel = 0;
    protected int suplevel = 0;
    protected int fractionlevel = 0;
    protected NemethTable table;

    static final int SUB = 0;
    static final int SUP = 1;
    public ArrayList<Integer> supsub = new ArrayList<>();
    
    static final int UNDER = 0;
    static final int OVER = 1;
    public ArrayList<Integer> overunder = new ArrayList<>();
    
    
    Box box;
    
    private boolean isOperator;
    
    public boolean isOperator() {
		return isOperator;
	}

	public void setOperator(boolean isOperator) {
		this.isOperator = isOperator;
	}

	public Expression() {
    	setOperator(false);
    }

    public Expression(NemethTable table) {
        this.table = table;
    }

    private Expression parent = null;

    public abstract void assignFractionLevel();

    public abstract void assignOtherLevels();

    public abstract String getBraille();

    // By default a box just contains characters...
    public Box createBox() {
    	
    	setBox(new Box(getBraille()));
    	
    	return this.box;
    }
    
    public Box getBox() {
    	return this.box;
    }
    
    public void setBox(Box b) {
    	this.box = b;
    }
  
    public String getLabel() {
    	return "";
    }
    
    void setParent(Expression exp){
        this.parent = exp;
    }

    Expression getParent(){
        return this.parent;
    }
    
  // Used for sup-sub delimiters end delimiters.
   Expression nextTo(Expression child) {
       return null;
   }

    // public abstract int getBaseline();

    public Expression getNext(){
        // Expression next = null;
        Expression mom = getParent();
        Expression child = this;

        if (mom == null)
            return null;
         
        return mom.nextTo(this);
        // while (next == null && mom != null) {
        //     next = mom.nextTo(child); // Or get sibling
        //     if (next != null) {
        //         break;
        //     }
        //     child = mom;
        //     mom = mom.getParent();
        // }
        // return next;
   }

//    ArrayList<> getNextSupSub(){
//        Expression nxt = getNext();
//        if (nxt!=null) {
//             return nxt.supsub
//        }
//        return null;
//    }
}
