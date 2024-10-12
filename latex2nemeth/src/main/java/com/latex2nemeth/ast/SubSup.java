package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;
import java.util.ArrayList;

public class SubSup extends AbstractSupSub {

	private Expression base, sup, sub;

	public SubSup(Expression base, Expression sub, Expression sup, NemethTable table) {
		super(table);
		this.base = base;
		this.sup = sup;
		this.sub = sub;

		// this.base.setParent(this);
		this.sub.setParent(this);
		this.sup.setParent(this);
	}

	@Override
	public void assignFractionLevel() {
		base.assignFractionLevel();
		sub.assignFractionLevel();
		sup.assignFractionLevel();
		this.fractionlevel = 0; // base.fractionleve
	}

	@Override
	public void assignOtherLevels() {
		base.sublevel = this.sublevel;
		base.suplevel = this.suplevel;
		base.sqrtlevel = this.sqrtlevel;

		sub.sublevel = this.sublevel + 1;
		sub.suplevel = this.suplevel;
		sub.sqrtlevel = this.sqrtlevel;

		sup.sublevel = this.sublevel;
		sup.suplevel = this.suplevel + 1;
		sup.sqrtlevel = this.sqrtlevel;

		base.supsub = this.supsub;
		sup.supsub = new ArrayList<>(this.supsub);
		sup.supsub.add(Expression.SUP);
		sub.supsub = new ArrayList<>(this.supsub);
		sub.supsub.add(Expression.SUB);

		base.assignOtherLevels();
		sub.assignOtherLevels();
		sup.assignOtherLevels();
	}

	@Override
	public String getBraille() {
		StringBuffer buffer = new StringBuffer();
		String subcode = table.getMathCode("\\sub");
		String supcode = table.getMathCode("\\superscript");
		String basecode = table.getMathCode("\\base");

		buffer.append(base.getBraille());

//        for (int i = 0; i <= sublevel; i++) {
//            buffer.append(subcode);
//        }

		for (int code : sub.supsub) {
			buffer.append(getSupSub(code));
		}

		buffer.append(sub.getBraille());

//        for (int i = 0; i <= suplevel; i++) {
//            buffer.append(supcode);
//        }

		for (int code : sup.supsub) {
			buffer.append(getSupSub(code));
		}
		
		buffer.append(sup.getBraille());

//        if (sublevel == 0) {
//            buffer.append(basecode);
//        }
		
		// Be careful!
		Expression next = this.getNext();
        if (next == null || next.supsub.size()==0) {
            if (supsub.size()==0)
                buffer.append(basecode);
        } 
        else {
             for (int code:next.supsub){
                buffer.append(getSupSub(code));
            }
        }
        
		return buffer.toString();
	}

}
