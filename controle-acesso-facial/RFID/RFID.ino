#include <SPI.h>
/* Include the RFID library */
#include <RFID.h>

/* Define the DIO used for the SDA (SS) and RST (reset) pins. */
#define SDA_DIO 10
#define RESET_DIO 9
/* Create an instance of the RFID library */
RFID RC522(SDA_DIO, RESET_DIO); 

void setup()
{ 
  Serial.begin(9600);
  /* Enable the SPI interface */
  SPI.begin(); 
  /* Initialise the RFID reader */
  RC522.init();
}

void loop()
{
  /* Has a card been detected? */
  if (RC522.isCard())
  {
    /* If so then get its serial number */
    RC522.readCardSerial();
    for(int i=0;i<5;i++)
    {
      // Serial.print(RC522.serNum[i], DEC);
      Serial.print(RC522.serNum[i], HEX); //to print card detail in Hexa Decimal format
    }
    Serial.println();
    Serial.println();
  }
  
  delay(1000);
}

