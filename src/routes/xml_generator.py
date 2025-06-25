from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import xml.etree.ElementTree as ET
from xml.dom import minidom
import logging

# 配置日誌
logging.basicConfig(level=logging.DEBUG)

xml_bp = Blueprint("xml", __name__)

@xml_bp.route("/generate-xml", methods=["POST"])
@cross_origin()
def generate_xml():
    try:
        data = request.json
        logging.debug(f"Received data: {data}")

        # 建立根元素
        root = ET.Element("twepadoc")

        # 建立doc元素
        doc = ET.SubElement(root, "doc")

        # 建立各個子元素
        elements = [
            "headline", "author", "pubname_chi", "pubname_eng", "language",
            "pubdate", "pageno", "category", "section", "score", "attr1",
            "attr2", "attr3", "attr4", "attr5", "attr6", "attr7", "url",
            "SourceStyle", "birdcage", "content", "Img", "docid", "image_cnt"
        ]

        for element_name in elements:
            value = data.get(element_name, "")

            if not value or str(value).strip() == "":
                value = ""

            # 特殊處理pubdate，確保格式正確
            if element_name == "pubdate":
                # 嘗試將日期轉換為YYYY-MM-DD格式，如果失敗則使用空字串
                try:
                    # 假設輸入的日期格式是YYYY-MM-DD
                    # 如果是其他格式，需要更複雜的解析邏輯
                    if value and len(value) == 10 and value[4] == '-' and value[7] == '-':
                        pass # 已經是正確格式
                    else:
                        logging.warning(f"Invalid pubdate format: {value}. Using empty string.")
                        value = ""
                except Exception as e:
                    logging.error(f"Error processing pubdate: {value}, {e}")
                    value = ""

            element = ET.SubElement(doc, element_name)
            element.text = str(value) # 確保所有值都是字串

        # 格式化XML
        rough_string = ET.tostring(root, "unicode")
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")

        # 移除第一行的XML宣告
        lines = pretty_xml.split("\n")
        if lines[0].startswith("<?xml"):
            lines = lines[1:]
        pretty_xml = "\n".join(lines)

        logging.debug("XML generated successfully.")
        return jsonify({
            "success": True,
            "xml": pretty_xml.strip()
        })

    except Exception as e:
        logging.error(f"Error generating XML: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

