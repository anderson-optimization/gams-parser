
p_max_pu_t(time,solar)=sum(sr$solar_sr(solar,sr),p_max_pu_t_sr(time,sr));


g(i)$(ord(i)>=2) = g(i-2) + g(i-1);


solar_sr(solar,sr)=1$(ord(solar)=ord(sr));