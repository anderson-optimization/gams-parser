
Equations            ProfitAcct              'Profit accounting equation' 
                     Available(resources)    'Resource availability limit'
                     Hirelimit(resources)    'Resource hiring limit';
     
 ProfitAcct..
      Profit
      =e= sum(products, Netreturns(products) * Production(products))
         - sum(resources, Hiredata(resources,"cost") * HireResource(resources))   ;
 
 Available(resources)..
      sum(products,
          Resourceusage(resources,products) * Production(products))
      =l= Endowments(resources) +  HireResource(resources);
      
 Hirelimit(resources)..
          HireResource(resources) =l= Hiredata(resources,"Maxavailable");