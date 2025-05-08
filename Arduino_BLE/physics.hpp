

#define U_PRESCALER(R1, R2) (static_cast<float>(R2) / (static_cast<float>(R1) + static_cast<float>(R2)))
#define ADC_LEVELS static_cast<float>(4095)
#define ADC_BITS 12
#define ADC_VREF 3.3f