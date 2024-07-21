# -*- coding: utf-8 -*-
"""dissertation-dallas-time-series.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1v-srW-4Myg-JfjQ5XnCCCALN_o7pyQ2r
"""

install.packages("shiny")
   install.packages("leaflet")
   install.packages("RColorBrewer")
   install.packages("tidyverse")
   install.packages("leaflet.extras")
   install.packages("lubridate")
   install.packages("gridExtra")
   install.packages("tidyr")
   install.packages("dplyr")
   install.packages("ggplot2")
   install.packages("ggridges")

library(ggmap)
library(shiny)
library(leaflet)
library(RColorBrewer)
library(tidyverse)
library(dplyr)
library(leaflet.extras)
library(lubridate)
library(gridExtra)
library(tidyr)
library(dplyr)
library(ggplot2)
library(ggridges)
install.packages("viridis")
library(viridis)

list.files(path = "/content/drive/MyDrive/dissertation/37-00049_UOF-P_2016_prepped.csv")

df <- read.csv("/content/drive/MyDrive/dissertation/37-00049_UOF-P_2016_prepped.csv",na.strings = c(""))
df = df[-1,]
head(df)
dim(df)

df$INCIDENT_DATE <- as.Date(df$INCIDENT_DATE, format = "%m/%d/%Y")
df$INCIDENT_DATE <- gsub("00","20",df$INCIDENT_DATE)
df$INCIDENT_DATE <- as.Date(df$INCIDENT_DATE, format = "%Y-%m-%d")
df$INCIDENT_TIME <- format(strptime(df$INCIDENT_TIME, "%I:%M:%S %p"), "%H:%M:%S")
df$INCIDENT_MONTH <- months(as.Date(df$INCIDENT_DATE))
df$INC_MONTH <-format(df$INCIDENT_DATE,"%m")
df$INCIDENT_HOUR <- as.numeric(substr(df$INCIDENT_TIME, 0, 2))
df$INCIDENT_DAY <- wday(df$INCIDENT_DATE, label=TRUE)
df$INC_HOUR <- substr(df$INCIDENT_TIME, 0, 2)
df$INC_DATE <- substr(df$INCIDENT_DATE, 9, 10)

## Create group of datas:

df_year <-  df %>%
  group_by(INCIDENT_DATE,INCIDENT_MONTH,INCIDENT_DAY) %>%
  summarize(count = n())

df_month <-  df %>%
  group_by(INC_MONTH) %>%
  summarize(count = n())

df_day <-  df %>%
  group_by(INCIDENT_DAY,INCIDENT_HOUR) %>%
  summarize(count = n())

df$INC_HOUR <- substr(df$INCIDENT_TIME, 0, 2)

df   %>% group_by(INC_HOUR) %>%
  summarize(avg =n()) -> df_hour_n

c1 <- ggplot(data = df_year, aes(INCIDENT_DATE, count)) +   geom_line(size=0.5, col="gray") +
geom_smooth(method = "loess", color = "red", span = 1/5) + theme_bw() + labs(x="Months ", y= "INCIDENT COUNTS", title="1.a Year vs Incidents")


r1 <- ggplot(df_month, aes(x=INC_MONTH, y =count, group=1)) + geom_line()  + geom_line( size = 1,colour ="steelblue") + labs(x="MONTHS OF 2016", y= "INCIDENT COUNTS", title="1.b Months vs  Incident Rates")  + theme_bw()


r2 <- ggplot(df_hour_n, aes(x = INC_HOUR, y = avg, group = "count")) + geom_line( size = 1, colour = "orange") + labs(x="HOURS IN A DAY", y= "INCIDENT COUNTS", title="1.c Hours vs  Incident Rates")+ theme_bw() +
theme(axis.text.x=element_text(angle=-90, vjust=0.5)) +

  labs(x = "Hour of the day", y = "count") + theme_bw()

r3 <- ggplot(df_year, aes(count)) +
  geom_density(alpha = 0.5, colour = "black", fill ="blue")+ labs(x="Incident counts", y= "Density", title="1.d Distribuion of incident rates") + theme_bw()


#grid.arrange(c1,r1,r2,r3,nrow=2)
c1
r1
r2
r3

library(ggridges)

###Multiplot function to join graphs:

multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)

  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)

  numPlots = length(plots)

  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }

  if (numPlots==1) {
    print(plots[[1]])

  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))

    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))

      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}




###Back to analysis:

p1 <- ggplot(df_year, aes(count, INCIDENT_MONTH, fill = INCIDENT_MONTH)) +

  geom_density_ridges(bandwidth = 0.1,size = 1) +
#  scale_fill_viridis(name = "T_max [°C]", option = "C") +
  scale_x_log10() +

  theme(legend.position = "none") +

  labs(x = "Number of Incidents", y = "Months")

#p1


p2 <- ggplot(df_year, aes(count, INCIDENT_DAY, fill = INCIDENT_DAY)) +

  geom_density_ridges(bandwidth = 0.1,size = 1) +

  scale_x_log10() +

  theme(legend.position = "none") +

  labs(x = "Number of Incidents", y = "Days")

#p2


layout <- matrix(c(1,1,2,2,2),1,5,byrow=TRUE)

multiplot(p1, p2, layout=layout)

df   %>%
  filter(SUBJECT_RACE == "Black"  | SUBJECT_RACE == "White" | SUBJECT_RACE == "Hispanic" ) %>%
  group_by(INCIDENT_DATE,INC_MONTH,SUBJECT_RACE) %>%
  summarize(avg =n()) -> df_dateh


g3 <- ggplot(df_dateh , aes(x = (INC_MONTH), y= avg, fill = INC_MONTH)) +

      geom_boxplot() +
      labs(x= 'days',y = 'Incident Rate',
           title = paste("Central Tendency of", ' Incident rate across SUBJECT RACE ')) +
      # theme_bw() +
  theme(legend.position="none") + facet_wrap(~SUBJECT_RACE)  +
    coord_cartesian(ylim = c(1, 12))
g3

df_srace <-  df %>%
  group_by(INC_MONTH,INCIDENT_MONTH,SUBJECT_RACE) %>%
  summarize(count = n())

df_orace <-  df %>%
  group_by(INC_MONTH,INCIDENT_MONTH,OFFICER_RACE) %>%
  summarize(count = n())



c1 <- ggplot() +
geom_line(data=subset(df_srace, SUBJECT_RACE=="Black" ) ,aes(y=count,x= INC_MONTH,colour="green",group=1),size=1 ) +
geom_line(data=subset(df_srace, SUBJECT_RACE=="Hispanic" ) ,aes(y=count,x= INC_MONTH,colour="red",group=1),size=1 ) +
  geom_line(data=subset(df_srace, SUBJECT_RACE=="White" ) ,aes(y=count,x= INC_MONTH,colour="orange",group=1),size=1 ) +
  scale_color_discrete(name = "Y series", labels = c("BLACKS", "WHITES","HISPANICS")) + labs(x="Months of 2016", y= "Counts", title=" Subject Race vs Incidents")  +
  scale_color_discrete(name = "Legend", labels = c("BLACKS", "WHITES","HISPANICS"))  + theme(axis.text.x=element_text( vjust=0.5),legend.position="bottom") +guides(colour=guide_legend(nrow=2))

c2 <- ggplot() +
  geom_line(data=subset(df_orace, OFFICER_RACE=="Black" ) ,aes(y=count,x= INC_MONTH,colour="green",group=1),size=1 ) +
  geom_line(data=subset(df_orace, OFFICER_RACE=="Hispanic" ) ,aes(y=count,x= INC_MONTH,colour="red",group=1),size=1 ) +
  geom_line(data=subset(df_orace, OFFICER_RACE=="White" ) ,aes(y=count,x= INC_MONTH,colour="orange",group=1),size=1 ) +
  scale_color_discrete(name = "Y series", labels = c("BLACKS", "WHITES","HISPANICS")) + labs(x="Months of 2016", title=" Officer Race vs Incident Handled Rates")  +
  scale_color_discrete(name = "Legend", labels = c("BLACKS", "WHITES","HISPANICS"))  + theme(axis.text.x=element_text( vjust=0.5),legend.position="bottom")+guides(colour=guide_legend(nrow=2))


layout <- matrix(c(1,1,1,1,2,2,2,2),3,8,byrow=TRUE)

multiplot(c1, c2, layout=layout)

df_div <-  df %>%
  group_by(INC_MONTH,DIVISION) %>%
  summarize(count = n())


#head(df_div,20)

library(scales)

ggplot(df_div, aes(x = INC_MONTH, y = count, group = 'count'))  + geom_line( aes(color= DIVISION), size = 1.2) + #labs(x="HOURS IN A DAY", y= "INCIDENT COUNTS", title=" Hours vs No of Incidents")
   facet_wrap(~ DIVISION,ncol=4) + #+ theme(axis.text.x=element_text(angle=-90, vjust=0.5)) +
theme(legend.position="none") +
  labs(x="Months ", y= "INCIDENT COUNTS", title=" Division vs Incidents")

df_subdes <-  df %>%
  group_by(INCIDENT_DATE,INCIDENT_MONTH,INCIDENT_DAY,SUBJECT_DESCRIPTION) %>%
  summarize(count = n())


library(viridis)
ggplot(subset(df_subdes,SUBJECT_DESCRIPTION != "FD-Motor Vehicle" & SUBJECT_DESCRIPTION != "NULL" & SUBJECT_DESCRIPTION != "FD-Animal" & SUBJECT_DESCRIPTION != "Animal"), aes(x = INCIDENT_DATE, y = SUBJECT_DESCRIPTION, fill = ..x..)) +

  geom_density_ridges_gradient(size=0.7,scale = 1, rel_min_height = 0.01, gradient_lwd = 1., bandwidth = 6,alpha = 1.5) +
   scale_fill_viridis(name = "Tail probability", direction = -1) +

  ggtitle("Distribution of SUBJECT DESCRIPTION") +

  labs(x = "months of 2016", y = "", fill = "Humidity") +

  theme_ridges(font_size = 13, grid = TRUE) +

  theme(legend.position = "none") +

  theme(axis.title.y = element_blank())

df$date <- substr(df$INCIDENT_DATE, 7, 8)
#df$date

df_monthdate <-  df %>%
  group_by(date, INC_MONTH) %>%
  summarize(count = n())
#df_monthdate
df_monthdate <- df_monthdate[complete.cases(df_monthdate), ]
ggplot(df_monthdate, aes(x= date, y=INC_MONTH,fill = count)) + geom_tile( ) +
geom_text(aes(date, INC_MONTH, label = count), color = "black", size = 3) + scale_y_discrete("Months",labels=c("January","February", "March", "April","May", "June","July","August", "September","October","November","December")) + labs(x="Days of Month", y= "Months", title=" Incident Rates across Dates and Months")+
  scale_fill_gradientn(colours = c("white", "red"))

df_monthday <-  df %>%
  group_by(INCIDENT_DAY, INC_MONTH) %>%
  summarize(count = n())

df_monthday <- df_monthday[complete.cases(df_monthday), ]

ggplot(df_monthday, aes(x= INCIDENT_DAY, y=INC_MONTH,fill = count)) + geom_tile( ) +
geom_text(aes(INCIDENT_DAY, INC_MONTH, label = count), color = "black", size = 4) + scale_y_discrete("Months",labels=c("January","February", "March", "April","May", "June","July","August", "September","October","November","December")) + labs(x="Days of Month", y= "Months", title=" Incident Rates across Dates and Months")+
  scale_fill_gradientn(colours = c("#3794bf", "#FFFFFF", "#df8640"))

df_subrace <-  df %>%
  group_by(SUBJECT_RACE, INC_MONTH) %>%
  summarize(count = n())

df_offrace <-  df %>%
  group_by(OFFICER_RACE, INC_MONTH) %>%
  summarize(count = n())

df_subrace <- df_subrace[complete.cases(df_subrace), ]
df_offrace <- df_offrace[complete.cases(df_offrace), ]

c1 <- ggplot(df_offrace, aes(x= INC_MONTH, y=OFFICER_RACE,fill = count)) + geom_tile( ) +
geom_text(aes(INC_MONTH, OFFICER_RACE, label = count), color = "black", size = 4) +# scale_y_discrete("Months",labels=c("January","February", "March", "April","May", "June","July","August", "September","October","November","December")) + labs(x="Days of Month", y= "Months", title=" Incident Rates across Dates and Months")+
  scale_fill_gradientn(colours = c("#3794bf", "#FFFFFF", "#df8640"))

c2 <- ggplot(df_subrace, aes(x= INC_MONTH, y=SUBJECT_RACE,fill = count)) + geom_tile( ) +
geom_text(aes(INC_MONTH, SUBJECT_RACE, label = count), color = "black", size = 4) + #scale_y_discrete("Months",labels=c("January","February", "March", "April","May", "June","July","August", "September","October","November","December")) + labs(x="Days of Month", y= "Months", title=" Incident Rates across Dates and Months")+
  scale_fill_gradientn(colours = c("#3794bf", "#FFFFFF", "#df8640"))

grid.arrange(c1,c2, nrow=2,ncol=1)