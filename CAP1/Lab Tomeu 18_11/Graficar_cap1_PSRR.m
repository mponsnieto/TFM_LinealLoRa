%root='C:\Users\Vicenç Salas\Desktop\CAP1\Lab Tomeu 18_11';
%% Prova deixant el gateway al despatx de'n Tomeu 
%  comparació del nombre de missatje rebut i enviat

filename = 'Datos 18_11';
sheet = 1;

dadesNRed = xlsread(filename,1);
dadesLoPy = xlsread(filename,'Hoja2');
counterNR=dadesNRed(:,19);
counterLoPy=dadesLoPy(:,3);
%%
PSRR=length(counterNR)/length(counterLoPy)*100; % PSRR=77.83%
aux=[1];
j=2;
k=2;
for (i=2:1:length(counterLoPy)-1)
    if j<length(counterNR)
        cNR=counterNR(j);
    else
        cNR=0;
    end
    if cNR/counterLoPy(i)==1
        aux=[aux 1];
        j=j+1;
    else
        aux =[aux 0];
    end
    
end
figure();
plot(1:1:length(counterLoPy)-1,aux);
ylim([-0.5,1.5]);
figure();
bar(aux);
ylim([-0.5,1.5]);




