package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;
import java.util.ArrayList;

public class Sub extends AbstractSupSub {

    private Expression base, sub;

    public Sub(Expression base, Expression sub, NemethTable table) {
        super(table);
        this.base = base;
        this.sub = sub;

        // this.base.setParent(this);
        this.sub.setParent(this);
//		sub.sublevel = base.sublevel + 1;
    }

    @Override
    // ?? What do we do here?
    public void assignFractionLevel() {
        base.assignFractionLevel();
        sub.assignFractionLevel();

        this.fractionlevel = 0; // base.fractionlevel;

//		sub.sublevel = base.sublevel + 1;
//		base.assignFractionLevels();
//		sub.assignFractionLevels();
    }

    @Override
    public void assignOtherLevels() {
        base.sublevel = this.sublevel;
        sub.sublevel = this.sublevel + 1;
        base.suplevel = this.suplevel;
        sub.suplevel = this.suplevel;
        base.sqrtlevel = this.sqrtlevel;
        sub.sqrtlevel = this.sqrtlevel;
    
        base.supsub = this.supsub;
        sub.supsub = new ArrayList<>(base.supsub);
    
        sub.supsub.add(Expression.SUB);

        base.assignOtherLevels();
        sub.assignOtherLevels();
    }

    @Override
    public String getBraille() {
        // Page 111
        StringBuffer buffer = new StringBuffer();
        String subcode = table.getMathCode("\\sub");
        String basecode = table.getMathCode("\\base");

        buffer.append(base.getBraille());
       
        // for (int i = 0; i <= sublevel; i++) {
        //     buffer.append(subcode);
        // }
        
        for (int code:sub.supsub){
            buffer.append(getSupSub(code));
        }

        buffer.append(sub.getBraille());
        
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
