export function formatDate(date: string) {
  if (!date) return '';

  const formatter = new Intl.DateTimeFormat('pt-BR', {
    dateStyle: 'short',
  });

  return formatter.format(new Date(date));
}

export function formatTime(date: string) {
  if (!date) return '';
  
  const formatter = new Intl.DateTimeFormat('pt-BR', {
    timeStyle: 'short',
  });

  return formatter.format(new Date(date));
}

export function formatMethod(method: number) {
  switch (method) {
    case 0:
      return 'Reconhecimento facial';
    case 1:
      return 'Sensor RFID';
    default:
      return 'Desconhecido';
  }
}

export function formatType(type: number) {
  switch (type) {
    case 0:
      return 'Entrada';
    case 1:
      return 'Saída';
    default:
      return 'Desconhecido';
  }
}
