import React from "react";
import { Link2, BookOpen } from "lucide-react";

interface SourceCardProps {
  page_content: string;
  page_image: string;
  relevance: number;
  title: string;
  type: string;
}

interface requestData {
  pdf_path: string;
  page_number: number;
}

export function SourceCard({
  page_content, // Page content as it is, we can show that on a tab on click after wards
  page_image,
  relevance,
  title,
  type,
}: SourceCardProps) {
  const [sourceContentFlag, setSourceContentFlag] = React.useState(false);
  const [showImage, setShowImage] = React.useState(false);
  const [sourceImage, setSourceImage] = React.useState<any>();
  const setSourceContentImageFlagfunction = async () => {
    if(!showImage) {
      const requestData: requestData = {
        pdf_path: title,
        page_number: relevance,
      };
      // console.log(requestData);
      const res = await fetch("http://127.0.0.1:5000/get_pdf_page", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });
      const result = await res.json();
      // console.log(result);
      const base64String = result.page_image;
      var image = new Image();
      image.src = "data:image/png;base64," + base64String;
      setSourceImage(image);
      // console.log(page_image);
      // const newTab = window.open();
      // if (newTab) {
      //   newTab.document.body.appendChild(image);
      //   image.style.maxWidth = "100%";
      //   image.style.maxHeight = "100%";
      //   image.style.objectFit = "contain";
      // } else {
      //   console.error(
      //     "Failed to open a new tab. Please allow pop-ups in your browser."
      //   );
      // }
      setShowImage(!showImage);
    }
    else{
      setShowImage(!showImage);
    }
    return
   
  };

  return (
    <>
      <div className="p-6 space-y-4">
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200 hover:border-blue-200 transition-colors">
          <div className="flex items-start justify-between">
            <div className="flex gap-3">
              <BookOpen className="text-blue-600 flex-shrink-0" size={20} />
              <div>
                <h3 className="font-medium text-gray-800 overflow-hidden">
                  {title}
                </h3>
                <p className="text-sm text-gray-600 mt-1">{type}</p>
                {/* <p className="text-xs text-gray-500 mt-1">Updated: {lastUpdated}</p> */}
                <button
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1 mt-2"
                  onClick={() => setSourceContentFlag(!sourceContentFlag)}
                >
                  <Link2 size={14} />
                  View Text
                </button>
                <button
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1 mt-2"
                  onClick={() => setSourceContentImageFlagfunction()}
                >
                  <Link2 size={14} />
                  View Page
                </button>
                {showImage && ( <img
                src={sourceImage.src}
                alt="Page Image"
                style={{ maxWidth: "100%", maxHeight: "100%", objectFit: "contain" }}
              />)}
              </div>
            </div>
            <span className="bg-blue-50 text-blue-700 text-xs font-medium px-2.5 py-1 rounded-full ">
              {relevance}
            </span>
          </div>
        </div>
      </div>
      {sourceContentFlag && (
        <div className="p-6 pt-0 space-y-4">
          <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200 hover:border-blue-200 transition-colors">
            <p
              className="text-sm text-gray-600 mt-1"
              style={{ whiteSpace: "pre-wrap", lineHeight: "1.5" }}
            >
              {page_content}
            </p>
          </div>
        </div>
      )}
    </>
  );
}
