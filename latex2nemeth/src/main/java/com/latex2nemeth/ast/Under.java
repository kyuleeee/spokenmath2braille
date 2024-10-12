package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;
import java.util.ArrayList;

public class Under extends AbstractOverUnder{

    private Expression base, under;

    public Under(Expression base, Expression under, NemethTable table) {
        super(table);
        this.base = base;
        this.under = under;

        // this.base.setParent(this);
        this.under.setParent(this);
//		sub.sublevel = base.sublevel + 1;
    }

    @Override
    // ?? What do we do here?
    public void assignFractionLevel() {
        base.assignFractionLevel();
        under.assignFractionLevel();

        this.fractionlevel = 0; // base.fractionlevel;

//		sub.sublevel = base.sublevel + 1;
//		base.assignFractionLevels();
//		sub.assignFractionLevels();
    }

    @Override
    public void assignOtherLevels() {
        base.sublevel = this.sublevel;
        under.sublevel = this.sublevel ;
        base.suplevel = this.suplevel;
        under.suplevel = this.suplevel;
        base.sqrtlevel = this.sqrtlevel;
        under.sqrtlevel = this.sqrtlevel;
    
        base.supsub = this.supsub;
        under.supsub = this.supsub;
        
        base.overunder = this.overunder;
        under.overunder= new ArrayList<>(base.overunder);
        under.supsub.add(Expression.UNDER);

        base.assignOtherLevels();
        under.assignOtherLevels();
    }

    @Override
    public String getBraille() {
        // Page 111
        StringBuffer buffer = new StringBuffer();
        String subcode = table.getMathCode("\\underset");
        String basecode = table.getMathCode("\\dot-end");

        buffer.append(base.getBraille());
       
        // for (int i = 0; i <= sublevel; i++) {
        //     buffer.append(subcode);
        // }
        
        for (int code:under.supsub){
            buffer.append(getOverUnder(code));
        }

        buffer.append(under.getBraille());
        
        Expression next = this.getNext();
        if (next == null || next.supsub.size()==0) {
            if (supsub.size()==0)
                buffer.append(basecode);
        } 
        else {
             for (int code:next.supsub){
                buffer.append(getOverUnder(code));
            }
        }

        // if (sublevel == 0) {
        //     buffer.append(basecode);
        // }
         
    //         Expression next = getNext();
    //         if ( next == null  || next.supsub.size() == 0)
    // //            if (getParent().supsub.size() == 0)
    //                  buffer.append(basecode);
    //         else {
    //             if (supsub.size()  == next.supsub.size())
    //                 for (int code:next.supsub){
    //                     buffer.append(getSupSub(code));
    //                 }
    //         }
          
    
        return buffer.toString();
    }

  

    


}
