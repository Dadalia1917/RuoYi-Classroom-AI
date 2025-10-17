/**
 * 时间格式化工具函数
 */

/**
 * 格式化日期
 * @param {Date} time 
 * @param {string} pattern 格式模式，如 'YYYY-mm-dd HH:MM:SS'
 * @returns {string}
 */
export function formatDate(time, pattern) {
  if (!time) return '';
  
  const date = new Date(time);
  
  const o = {
    'Y+': date.getFullYear(),
    'm+': date.getMonth() + 1,
    'd+': date.getDate(),
    'H+': date.getHours(),
    'M+': date.getMinutes(),
    'S+': date.getSeconds(),
  };

  for (const k in o) {
    const ret = new RegExp('(' + k + ')').exec(pattern);
    if (ret) {
      pattern = pattern.replace(ret[1], ret[1].length === 1 ? o[k] : ('00' + o[k]).substr(('00' + o[k]).length - ret[1].length));
    }
  }
  
  return pattern;
}

/**
 * 解析时间
 * @param {*} time 
 * @param {*} cFormat 
 * @returns 
 */
export function parseTime(time, cFormat) {
  if (arguments.length === 0 || !time) {
    return null;
  }
  
  const format = cFormat || '{y}-{m}-{d} {h}:{i}:{s}';
  let date;
  
  if (typeof time === 'object') {
    date = time;
  } else {
    if ((typeof time === 'string')) {
      if ((/^[0-9]+$/.test(time))) {
        time = parseInt(time);
      } else {
        time = time.replace(new RegExp(/-/gm), '/');
      }
    }
    if ((typeof time === 'number') && (time.toString().length === 10)) {
      time = time * 1000;
    }
    date = new Date(time);
  }
  
  const formatObj = {
    y: date.getFullYear(),
    m: date.getMonth() + 1,
    d: date.getDate(),
    h: date.getHours(),
    i: date.getMinutes(),
    s: date.getSeconds(),
    a: date.getDay()
  };
  
  const time_str = format.replace(/{([ymdhisa])+}/g, (result, key) => {
    const value = formatObj[key];
    if (key === 'a') {
      return ['日', '一', '二', '三', '四', '五', '六'][value];
    }
    return value.toString().padStart(2, '0');
  });
  
  return time_str;
}
