filename = 'ProvaLopy2LopyPotencies';
sheet = 1;

dadesC1 = xlsread(filename,1);
dadesC2 = xlsread(filename,2);
time=dadesC1(:,1);
volt_C1=dadesC1(:,2);
volt_C2=dadesC2(:,2);

t=time;
y1=5-volt_C1;
y2=volt_C2;

y1lim = [0,0.3];
y1ticks = [0:0.05:1];
y1string = 'consum lopy (A)';

y2lim = [-1,3] ;
y2ticks = [-6:0.5:6];
y2string = 'pin p12 (V)';

x1lim = [4,10];
x1ticks = [1.5:0.3:25];
x1string ='time (s)';

color1 = [0 0.2 0.9];
color2 = [0 0.5 0.1];


figure1 = figure(1);

axes1 = axes('Parent',figure1,...
'YTick',y1ticks,...
'XTick',[],...
'ColorOrder',[color1; color1],...
'YColor',color1,...
'Fontsize',10);
xlim(axes1,x1lim);
ylim(axes1,y1lim);
box(axes1,'on');
hold(axes1,'all');
plot(t,y1,'Parent',axes1,'LineWidth',1);
ylabel(y1string,'Color',color1);

axes2 = axes('Parent',figure1,...
'YTick',y2ticks,...
'XTick',x1ticks,...
'ColorOrder',[color2; color2],...
'YColor',color2,...
'Color','none',...
'Fontsize',10,...
'YAxisLocation','right');
xlim(axes2,x1lim);
ylim(axes2,y2lim);
hold(axes2,'all');
plot(t,y2,'Parent',axes2,'LineWidth',1);
ylabel(y2string,'Color',color2);
xlabel(x1string);
title('Consum del sistema enviant per raw-LoRa a distintes pot�ncies ');