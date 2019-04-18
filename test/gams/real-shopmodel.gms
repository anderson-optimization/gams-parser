Set       products  'Items produced' 
              / Chairs, Tables, Dressers /
          resources  'Resources limiting production'
              / RawWood, Labor, WarehouseSpace/
          hireterms  'Resource hiring terms'
              / Cost, Maxavailable /;

Parameter Netreturns(products)  'Net returns per unit produced'
              / Chairs 19, Tables 50, Dressers 75 /
          Endowments(resources) 'Amount of each resource available'
              / RawWood 700, Labor 1000, WarehouseSpace 240 /;

Table     Resourceusage(resources,products) 'Resource usage per unit produced'
                          Chairs   Tables  Dressers
          RawWood            8        20      32
          Labor             12        32      45
          WarehouseSpace     4        12      10   ;
  
Table     Hiredata(resources,hireterms)  'Resource hiring data'
                          Cost   Maxavailable
          RawWood            3        200
          Labor             12        120
          WarehouseSpace     4        112;

Positive Variables   Production(products)    'Number of units produced'
                     HireResource(resources) 'Resources hired';          
Variables            Profit                  'Total sum of net returns' ;

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

Model resalloc /all/;

solve reasalloc using LP maximizing Profit;