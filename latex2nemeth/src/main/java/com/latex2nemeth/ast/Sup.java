package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;
import java.util.ArrayList;

public class Sup extends AbstractSupSub {

    private Expression base, sup;

    public Sup(Expression base, Expression sup, NemethTable table) {
        super(table);
        this.base = base;
        this.sup = sup;
//		sup.suplevel = base.suplevel + 1;

        // this.base.setParent(this);
        this.sup.setParent(this);
    }

    @Override
    public void assignFractionLevel() {
        base.assignFractionLevel();
        sup.assignFractionLevel();
        this.fractionlevel = 0; //base.fractionlevel;
    }

    @Override
    public void assignOtherLevels() {
        base.sublevel = this.sublevel;
        sup.suplevel = this.suplevel + 1;
        base.suplevel = this.suplevel;
        sup.sublevel = this.sublevel;
        base.sqrtlevel = this.sqrtlevel;
        sup.sqrtlevel = this.sqrtlevel;

        base.supsub = this.supsub;
        sup.supsub = new ArrayList<>(this.supsub);
        sup.supsub.add(Expression.SUP);

        base.assignOtherLevels();
        sup.assignOtherLevels();
    }

    @Override
    public String getBraille() {
        // Page 111
        StringBuffer buffer = new StringBuffer();
        String supcode = table.getMathCode("\\superscript");
        String basecode = table.getMathCode("\\base");


        buffer.append(base.getBraille());
      
      /*
         for (int i = 0; i <= suplevel; i++) {
             buffer.append(supcode);
         }
    */
   
        for (int code:sup.supsub){
            buffer.append(getSupSub(code));
        }

        buffer.append(sup.getBraille());
    
        //TODO: complete what happens after the superscript...
        
        // if (suplevel == 0) {
        //     buffer.append(basecode);
        // }
       
        Expression next = this.getNext();
        if (next == null || next.supsub.size()==0) {
            if (supsub.size() == 0)
                buffer.append(basecode);
        } 
        else {
             for (int code:next.supsub){
                buffer.append(getSupSub(code));
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
