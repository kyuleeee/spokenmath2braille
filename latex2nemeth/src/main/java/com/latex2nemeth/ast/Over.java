package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;
import java.util.ArrayList;

public class Over extends AbstractOverUnder{

    private Expression base, over;

    public Over(Expression base, Expression over, NemethTable table) {
        super(table);
        this.base = base;
        this.over = over;
//		sup.suplevel = base.suplevel + 1;

        // this.base.setParent(this);
        this.over.setParent(this);
    }

    @Override
    public void assignFractionLevel() {
        base.assignFractionLevel();
        over.assignFractionLevel();
        this.fractionlevel = 0; //base.fractionlevel;
    }

    @Override
    public void assignOtherLevels() {
        base.sublevel = this.sublevel;
        over.suplevel = this.suplevel ;
        base.suplevel = this.suplevel;
        over.sublevel = this.sublevel;
        base.sqrtlevel = this.sqrtlevel;
        over.sqrtlevel = this.sqrtlevel;

        base.supsub = this.supsub;
        over.supsub = new ArrayList<>(this.supsub);//?
        
        base.overunder = this.overunder;
        over.overunder = new ArrayList<>(this.overunder);
        over.overunder.add(Expression.OVER);

        base.assignOtherLevels();
        over.assignOtherLevels();
    }

    @Override
    public String getBraille() {
        // Page 111
        StringBuffer buffer = new StringBuffer();
        String supcode = table.getMathCode("\\overset");
        String basecode = table.getMathCode("\\dot-end");

        buffer.append(base.getBraille());
      
      /*
         for (int i = 0; i <= suplevel; i++) {
             buffer.append(supcode);
         }
    */
   
        for (int code:over.supsub){
            buffer.append(getOverUnder(code));
        }

        buffer.append(over.getBraille());
    
        //TODO: complete what happens after the superscript...
        
        // if (suplevel == 0) {
        //     buffer.append(basecode);
        // }
       
        Expression next = this.getNext();
        if (next == null || next.overunder.size()==0) {
            if (overunder.size() == 0)
                buffer.append(basecode);
        } 
        else {
             for (int code:next.overunder){
                buffer.append(getOverUnder(code));
            }
        }


        // Expression next = getNext();
        //  if (next == null || next.supsub.size() == 0)
        //     if (supsub.size() == 0)
        //         buffer.append(basecode);
        // else {
        //       if (supsub.size() == next.supsub.size())
        //      for (int code:next.supsub){
        //             buffer.append(getSupSub(code));
        //     }
        // }
        return buffer.toString();
    }


}
