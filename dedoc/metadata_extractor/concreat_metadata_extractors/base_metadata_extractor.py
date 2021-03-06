import os
from typing import Optional

from dedoc.data_structures.document_content import DocumentContent
from dedoc.data_structures.document_metadata import DocumentMetadata
from dedoc.data_structures.parsed_document import ParsedDocument
from dedoc.utils import get_file_mime_type
from dedoc.metadata_extractor.concreat_metadata_extractors.abstract_metadata_extractor import AbstractMetadataExtractor


class BaseMetadataExtractor(AbstractMetadataExtractor):
    """
    Base class for metadata extractor. Inheritor should implement two methods: can_extract and add_metadata
    """

    def can_extract(self,
                    doc: Optional[DocumentContent],
                    directory: str,
                    filename: str,
                    converted_filename: str,
                    original_filename: str,
                    parameters: dict = None) -> bool:
        """
        check if this extractor can handle given file. Return True if can handle and False otherwise

        :type doc: document content
        :type directory: path to directory where original file and converted file are located
        :type filename: name of file after rename (for example 23141.doc)
        :type converted_filename: name of file after rename and conversion (for example 23141.docx)
        :type original_filename: file name before rename
        :type parameters: additional parameters

        """
        return True

    def add_metadata(self,
                     doc: Optional[DocumentContent],
                     directory: str,
                     filename: str,
                     converted_filename: str,
                     original_filename: str,
                     parameters: dict = None) -> ParsedDocument:
        """
        add metadata to doc. Use this method only if this extractor can_extract this file

        :type doc: document content
        :type directory: path to directory where original file and converted file are located
        :type filename: name of file after rename (for example 23141.doc)
        :type converted_filename: name of file after rename and conversion (for example 23141.docx)
        :type original_filename: file name before rename
        :type parameters: additional parameters

        """
        if parameters is None:
            parameters = {}
        meta_info = self._get_base_meta_information(directory, filename, original_filename, parameters)
        metadata = DocumentMetadata(
            file_name=meta_info["file_name"],
            file_type=meta_info["file_type"],
            size=meta_info["size"],
            access_time=meta_info["access_time"],
            created_time=meta_info["created_time"],
            modified_time=meta_info["modified_time"]
        )
        parsed_document = ParsedDocument(metadata=metadata, content=doc)
        return parsed_document

    def _get_base_meta_information(self, dir: str, filename: str, name_actual: str, parameters: dict) -> dict:
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(os.path.join(dir, filename))
        meta = {
            "file_name": name_actual,
            "file_type": get_file_mime_type(os.path.join(dir, filename)),
            "size": size,  # in bytes
            "access_time": atime,
            "created_time": ctime,
            "modified_time": mtime
        }

        return meta
