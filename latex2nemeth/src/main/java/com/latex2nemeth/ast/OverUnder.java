package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;
import java.util.ArrayList;

public class OverUnder extends AbstractOverUnder{

	private Expression base, over, under;

	public OverUnder(Expression base, Expression under, Expression over, NemethTable table) {
		super(table);
		this.base = base;
		this.over = over;
		this.under= under;

		// this.base.setParent(this);
		this.under.setParent(this);
		this.over.setParent(this);
	}

	@Override
	public void assignFractionLevel() {
		base.assignFractionLevel();
		over.assignFractionLevel();
		under.assignFractionLevel();
		this.fractionlevel = 0; // base.fractionleve
	}

	@Override
	public void assignOtherLevels() {
		base.sublevel = this.sublevel;
		base.suplevel = this.suplevel;
		base.sqrtlevel = this.sqrtlevel;

		under.sublevel = this.sublevel;
		under.suplevel = this.suplevel;
		under.sqrtlevel = this.sqrtlevel;

		over.sublevel = this.sublevel;
		over.suplevel = this.suplevel;
		over.sqrtlevel = this.sqrtlevel;

		base.supsub = this.supsub;
		over.supsub = this.supsub;
		under.supsub = this.supsub;
		
		over.overunder= new ArrayList<>(this.overunder);
		over.overunder.add(Expression.OVER);
		under.overunder = new ArrayList<>(this.overunder);
		under.overunder.add(Expression.UNDER);
		
		base.assignOtherLevels();
		over.assignOtherLevels();
		under.assignOtherLevels();
}

	@Override
	public String getBraille() {
		StringBuffer buffer = new StringBuffer();
	
		String basecode = table.getMathCode("\\dot-end");

		buffer.append(base.getBraille());
		
		for (int code : under.overunder) {
			buffer.append(getOverUnder(code));
		}

		buffer.append(under.getBraille());


		for (int code : over.overunder) {
			buffer.append(getOverUnder(code));
		}
		
		buffer.append(over.getBraille());

//        if (sublevel == 0) {
//            buffer.append(basecode);
//        }
		
		// Be careful!
//		if (!(this.getParent() instanceof Sideset)) {
			Expression next = this.getNext();
			if (next == null || next.overunder.size()==0) {
				if (overunder.size()==0)
					buffer.append(basecode);
			} 
			else {
				for (int code:next.overunder){
					buffer.append(getOverUnder(code));
				}
			}
//		}
        
		return buffer.toString();
	}

}
