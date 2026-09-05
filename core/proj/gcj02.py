# -*- coding:utf-8 -*-

#  ***** GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  ***** GPL LICENSE BLOCK *****

import math

from .reproj import webMercToLonLat, lonLatToWebMerc

# GCJ-02 (火星坐标) 与 WGS84 之间的转换
# 算法为公开标准算法 (参考 eviltransform / coordtransform 等开源实现)
# 高德(AMap)、腾讯等国内地图瓦片使用 GCJ-02 坐标系, 与 WGS84 存在约 100~600 米的系统性偏移

A = 6378245.0  # Krasovsky 1940 椭球长半轴
EE = 0.00669342162296594323  # 第一偏心率平方


def _outOfChina(lng, lat):
	return not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271)


def _transformLat(x, y):
	ret = -100.0 + 2.0*x + 3.0*y + 0.2*y*y + 0.1*x*y + 0.2*math.sqrt(abs(x))
	ret += (20.0*math.sin(6.0*x*math.pi) + 20.0*math.sin(2.0*x*math.pi)) * 2.0/3.0
	ret += (20.0*math.sin(y*math.pi) + 40.0*math.sin(y/3.0*math.pi)) * 2.0/3.0
	ret += (160.0*math.sin(y/12.0*math.pi) + 320.0*math.sin(y*math.pi/30.0)) * 2.0/3.0
	return ret


def _transformLng(x, y):
	ret = 300.0 + x + 2.0*y + 0.1*x*x + 0.1*x*y + 0.1*math.sqrt(abs(x))
	ret += (20.0*math.sin(6.0*x*math.pi) + 20.0*math.sin(2.0*x*math.pi)) * 2.0/3.0
	ret += (20.0*math.sin(x*math.pi) + 40.0*math.sin(x/3.0*math.pi)) * 2.0/3.0
	ret += (150.0*math.sin(x/12.0*math.pi) + 300.0*math.sin(x/30.0*math.pi)) * 2.0/3.0
	return ret


def wgs84_to_gcj02(lng, lat):
	"""WGS84 经纬度(十进制度) -> GCJ-02 经纬度"""
	if _outOfChina(lng, lat):
		return lng, lat
	dLat = _transformLat(lng - 105.0, lat - 35.0)
	dLng = _transformLng(lng - 105.0, lat - 35.0)
	radLat = lat / 180.0 * math.pi
	magic = math.sin(radLat)
	magic = 1 - EE * magic * magic
	sqrtMagic = math.sqrt(magic)
	dLat = (dLat * 180.0) / ((A * (1 - EE)) / (magic * sqrtMagic) * math.pi)
	dLng = (dLng * 180.0) / (A / sqrtMagic * math.cos(radLat) * math.pi)
	return lng + dLng, lat + dLat


def gcj02_to_wgs84(lng, lat):
	"""GCJ-02 经纬度(十进制度) -> WGS84 经纬度 (迭代近似, 精度 < 1e-9 度)"""
	if _outOfChina(lng, lat):
		return lng, lat
	wgsLat, wgsLng = lat, lng
	for _ in range(30):
		mgLng, mgLat = wgs84_to_gcj02(wgsLng, wgsLat)
		dLat = mgLat - lat
		dLng = mgLng - lng
		wgsLat -= dLat
		wgsLng -= dLng
		if abs(dLat) < 1e-9 and abs(dLng) < 1e-9:
			break
	return wgsLng, wgsLat


def _shiftBbox(bbox, reverse=False):
	"""把 Web Mercator(EPSG:3857) bbox 在 WGS84 与 GCJ-02 之间转换"""
	xmin, ymin, xmax, ymax = bbox
	corners = [(xmin, ymin), (xmax, ymin), (xmin, ymax), (xmax, ymax)]
	lons_lats = [webMercToLonLat(x, y) for x, y in corners]
	if not reverse:
		shifted = [wgs84_to_gcj02(lon, lat) for lon, lat in lons_lats]
	else:
		shifted = [gcj02_to_wgs84(lon, lat) for lon, lat in lons_lats]
	merc = [lonLatToWebMerc(lon, lat) for lon, lat in shifted]
	xs = [p[0] for p in merc]
	ys = [p[1] for p in merc]
	return (min(xs), min(ys), max(xs), max(ys))


def shiftBboxToGcj02(bbox):
	"""EPSG:3857 WGS84 Web Mercator bbox -> GCJ-02 Web Mercator bbox (同一瓦片编号体系)"""
	return _shiftBbox(bbox, reverse=False)


def shiftBboxToWgs84(bbox):
	"""EPSG:3857 GCJ-02 Web Mercator bbox -> WGS84 Web Mercator bbox"""
	return _shiftBbox(bbox, reverse=True)
