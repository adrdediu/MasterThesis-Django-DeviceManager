'use client';

import React from 'react';

interface CustomLinkProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  href: string;
  children: React.ReactNode;
}

const CustomLink: React.FC<CustomLinkProps> = ({ href, children, ...props }) => {
  const fullHref = href.startsWith('/') ? `/nextjs${href}` : `/nextjs/${href}`;

  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    window.parent.postMessage({ type: 'NAVIGATE', url: fullHref }, '*');
  };

  return (
    <a href={fullHref} onClick={handleClick} {...props}>
      {children}
    </a>
  );
};

export default CustomLink;
